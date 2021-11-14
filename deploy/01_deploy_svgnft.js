const { networkConfig } = require("../helper-hardhat-config");
const fs = require('fs')

module.exports = async ({
    getNamedAccounts,
    deployments,
    getChainId
}) => {
    const { deploy, log } = deployments;
    const { deployer } = await getNamedAccounts();
    const chainId = await getChainId();

    log("-------------------------");

    // Deploy the smart contract on the blockchain
    const SVGNFT = await deploy("SVGNFT", { from: deployer, log: true });
    log(`SVGNFT contract deployed to ${SVGNFT.address}`);

    // Get all the information of the deployed smart contract
    const svgNFTContract = await ethers.getContractFactory("SVGNFT");
    const accounts = await hre.ethers.getSigners();
    const signer = accounts[0];
    const svgNFT = new ethers.Contract(SVGNFT.address, svgNFTContract.interface, signer);
    const networkName = networkConfig[chainId]['name'];

    // Verify the smart contract on etherscan
    log(`Verify with: $ npx hardhat verify --network ${networkName} ${svgNFT.address}`);

    // Mint an NFT
    let svg = fs.readFileSync("./generated/example.svg", {encoding: "utf8"});
    tx = await svgNFT.mint(svg);
    await tx.wait(1); // wait for 1 block
    log(`SVGNFT #0 minted! View the tokenURI here: ${await svgNFT.tokenURI(0)}`);
}