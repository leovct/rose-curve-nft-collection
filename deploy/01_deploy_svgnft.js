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

    // Mint two NFTs
    await mint(svgNFT, log, "./generated/example.svg", 0);
    await mint(svgNFT, log, "./generated/example-animated.svg", 1)
}

async function mint(contract, log, svgPath, tokenId) {
    let svg = fs.readFileSync(svgPath, {encoding: "utf8"});
    tx = await contract.mint(svg);
    await tx.wait(1); // wait for 1 block
    log(`\nSVGNFT #${tokenId} minted! View the tokenURI here: ${await contract.tokenURI(tokenId)}`);
}
