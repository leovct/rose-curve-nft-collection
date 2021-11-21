const utils = require("./utils")

module.exports = async ({
    getNamedAccounts,
    deployments,
    getChainId
}) => {
    const { deploy, log } = deployments
    const { deployer } = await getNamedAccounts()
    const chainId = await getChainId()

    log("-------------------------\n")

    // Check if we are deploying on a local or a real blockchain
    if (chainId == 31337) {
        // Deploying on a local blockchain, thus we need to deploy mocks
        log("Local network detected! Deploying mocks...")

        // Deploy the mock Link contract on the blockchain
        linkContract = {
            name: "LinkToken",
            deployer: deployer,
            args: null,
            enableLogs: true,
            address: null
        }
        log()
        linkContract.address = await utils.deployContract(log, deploy, linkContract)

        // Deploy the mock VRFCoordinator contract on the blockchain
        vrfCoordinatorContract = {
            name: "VRFCoordinatorMock",
            deployer: deployer,
            args: [linkContract.address],
            enableLogs: true
        }
        log()
        await utils.deployContract(log, deploy, vrfCoordinatorContract)
    } else {
        log("Real blockchain detected, no need to deploy mocks!")
    }
}

module.exports.tags = ['all', 'mock', 'rsvg', 'rose']
