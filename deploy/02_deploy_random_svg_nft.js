const { networkConfig } = require("../helper-hardhat-config")
const utils = require("./utils")

module.exports = async ({
    getNamedAccounts,
    deployments,
    getChainId
}) => {
    const { deploy, get, log } = deployments
    const { deployer } = await getNamedAccounts()
    const chainId = await getChainId()

    // Define the Chainlink VRF parameters
    let [linkTokenAddress, vrfCoordinatorAddress, keyHash, fee] = 
        await utils.getChainlinkVRFParameters(get, networkConfig, chainId)

    log("\n-------------------------\n")

    // Define the RandomSVGNFT smart contract parameters
    contract = {
        name: 'RandomSVGNFT',
        args: [vrfCoordinatorAddress, linkTokenAddress, keyHash, fee],
        deployer: deployer,
        enableLogs: true,
    }

    // Deploy the contract on the blockchain
    contract.address = await utils.deployContract(log, deploy, contract)

    // Verify the contract on etherscan
    const networkName = networkConfig[chainId]['name']
    log()
    utils.verifyContract(log, networkName, contract)

    // Get all the information of the deployed contract
    const accounts = await hre.ethers.getSigners()
    const signer = accounts[0]
    contract.interface = (await ethers.getContractFactory(contract.name)).interface
    contract.instance = new ethers.Contract(contract.address, contract.interface, signer)

    // Mint some NFTs
    await mint(log, chainId, linkTokenAddress, fee, contract.instance, contract.address, contract.name, signer)
    await mint(log, chainId, linkTokenAddress, fee, contract.instance, contract.address, contract.name, signer)
}

async function mint(log, chainId, linkTokenAddress, fee, contract, contractAddress, contractName, signer) {
    // Fund the smart contract with some $LINK to interact with Chainlink VRF
    log()
    await utils.fundContractWithLinkToken(log, linkTokenAddress, fee, contractAddress, contractName, signer)

    // Request to mint the NFT
    startMint_tx = await contract.startMint({ gasLimit: 300_000 })
    let receipt = await startMint_tx.wait(1)
    let tokenId = receipt.events[3].topics[2]
    log(`\n${contractName} #${parseInt(tokenId, 16)} requested!`)

    // Wait for Chainlink VRF to send the random number associated to the tokenId
    // Check if we are deploying on a local or a real blockchain
    log('Waiting for the Chainlink VRF node to respond...')
    if (chainId == 31337) {
        // Deploying on a local blockchain, thus we need to mock the Chainlink VRF answer
        const vrfCoordinatorMockContract = await deployments.get('VRFCoordinatorMock')
        vrfCoordinator = await ethers.getContractAt('VRFCoordinatorMock', vrfCoordinatorMockContract.address, signer)

        // Send a fake random number
        let vrfAnswer_tx = await vrfCoordinator.callBackWithRandomness(receipt.logs[3].topics[1], 77777, contract.address)
        await vrfAnswer_tx.wait(1)
    } else {
        // Wait for the Chainlink VRF node to respond
        await new Promise(r => setTimeout(r, 180_000))
    }

    // Finish the mint by calling the finishMint function
    log(`Random number received!`)
    finishMint_tx = await contract.finishMint(tokenId, { gasLimit: 2_000_000 })
    await finishMint_tx.wait(1)

    log(`${contractName} #${parseInt(tokenId, 16)} minted!\nView the tokenURI here: ${await contract.tokenURI(tokenId)}`)
}

module.exports.tags = ['all', 'rsvg']
