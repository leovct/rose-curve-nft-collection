async function deployContract(log, deploy, contract) {
    const deployedContract = await deploy(contract.name, {
        from: contract.deployer,
        args: contract.args,
        log: contract.enableLogs
    })
    log(`${contract.name} contract successfully deployed!`)
    return deployedContract.address
}

function verifyContract(log, networkName, contract) {
    if (networkName !== "localhost") {
        if (contract.args) {
            log(`Verify with: $ npx hardhat verify --network ${networkName} ${contract.address} ${contract.args.toString().replace(/,/g, " ")}`)
        } else {
            log(`Verify with: $ npx hardhat verify --network ${networkName} ${contract.address}`)
        }
    }
}

async function getChainlinkVRFParameters(get, networkConfig, chainId) {
    // Get the parameters to work with Chainlink VRF
    // Check if we are deploying on a local or a real blockchain
    let linkTokenAddress, vrfCoordinatorAddress
    if (chainId == 31337) {
        // Deploying on a local blockchain, thus we need to deploy mocks
        // This is already done by the 00_deploy_mocks.js script
        // We just need to get the address of the deployed mocks
        let linkToken = await get('LinkToken')
        linkTokenAddress = linkToken.address

        let vrfCoordinatorMock = await get('VRFCoordinatorMock')
        vrfCoordinatorAddress = vrfCoordinatorMock.address
    } else {
        // Deploying on a real blockchain, get the parameters from the networkConfig
        linkTokenAddress = networkConfig[chainId]['linkTokenAddress']
        vrfCoordinatorAddress = networkConfig[chainId]['vrfCoordinatorAddress']
    }
    const keyHash = networkConfig[chainId]['keyHash']
    const fee = networkConfig[chainId]['fee']
    return [linkTokenAddress, vrfCoordinatorAddress, keyHash, fee]
}

async function fundContractWithLinkToken(log, linkTokenAddress, fee, contractAddress, contractName, signer) {
    const linkTokenContract = await ethers.getContractFactory('LinkToken')
    const linkToken = new ethers.Contract(linkTokenAddress, linkTokenContract.interface, signer)
    let fund_tx = await linkToken.transfer(contractAddress, fee)
    await fund_tx.wait(1)

    log(`${contractName} contract (${contractAddress}) successfully funded with ${fee * 1e-18} $LINK token(s) (${linkTokenAddress})!`)
    linkBalance = await linkToken.balanceOf(contractAddress)
    log(`The contract now has a balance of ${parseInt(linkBalance._hex, 16) * 1e-18} $LINK token(s)`)
}

module.exports = { deployContract, verifyContract, getChainlinkVRFParameters, fundContractWithLinkToken }
