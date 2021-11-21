const { networkConfig } = require("../helper-hardhat-config")
const utils = require("./utils")
const fs = require('fs')

module.exports = async ({
    getNamedAccounts,
    deployments,
    getChainId
}) => {
    const { deploy, log } = deployments
    const { deployer } = await getNamedAccounts()
    const chainId = await getChainId()

    log("-------------------------\n")

    // Define the SVGNFT smart contract parameters
    contract = {
        name: "SVGNFT",
        deployer: deployer,
        args: null,
        enableLogs: true,
        address: null,
        interface: null,
        instance: null,
    }

    // Deploy the contract on the blockchain
    contract.address = await utils.deployContract(log, deploy, contract)

    // Verify the contract on etherscan
    const networkName = networkConfig[chainId]['name']
    utils.verifyContract(log, networkName, contract)

    // Get all the information of the deployed smart contract
    const accounts = await hre.ethers.getSigners()
    const signer = accounts[0]
    contract.interface = (await ethers.getContractFactory(contract.name)).interface
    contract.instance = new ethers.Contract(contract.address, contract.interface, signer)

    // Mint two NFTs
    await mint(log, contract.instance, "./svg/deploy/circle.svg", 0)
    await mint(log, contract.instance, "./svg/deploy/animated-squares.svg", 1)
}

async function mint(log, contract, svgPath, tokenId) {
    let svg = fs.readFileSync(svgPath, { encoding: "utf8" })
    tx = await contract.mint(svg)
    await tx.wait(1)
    log(`\nSVGNFT #${tokenId} minted!\nView the tokenURI here: ${await contract.tokenURI(tokenId)}`)
}

module.exports.tags = ['all', 'svg']
