-- Exported from QuickDBD: https://www.quickdatatabasediagrams.com/
-- Link to schema: https://app.quickdatabasediagrams.com/#/schema/apBRv5MRjUGiOmAYVWdSug
-- NOTE! If you have used non-SQL datatypes in your design, you will have to change these here.

-- Modify this code to update the DB schema diagram.
-- To reset the sample schema, replace everything with
-- two dots ('..' - without quotes).

CREATE TABLE `blockchain` (
    `index` bigint  NOT NULL ,
    `previous_hash` string  NOT NULL ,
    `transactions` string ,
    `proof` bigint ,
    `timestamp` float  NOT NULL ,
    PRIMARY KEY (
        `index`
    ),
    FOREIGN KEY (transactions) REFERENCES transactions(signature)
);

CREATE TABLE `wallet` (
    `public_key` string  NOT NULL ,
    PRIMARY KEY (
        `public_key`
    )
);

CREATE TABLE `transactions` (
    `sender` string  NOT NULL ,
    `recipient` string  NOT NULL ,
    `amount` float  NOT NULL ,
    `signature` string  NOT NULL ,
    PRIMARY KEY (
        `signature`
    ), 
    FOREIGN KEY (sender) REFERENCES `wallet` (`public_key`), 
    FOREIGN KEY (recipient) REFERENCES `wallet` (`public_key`) 
);

CREATE TABLE `peer_nodes` (
    `id` string  NOT NULL ,
    `public_key` string  NOT NULL ,
    PRIMARY KEY (
        `id`
    ),
    FOREIGN KEY (public_key) REFERENCES wallet(public_key)
);



# Modify this code to update the DB schema diagram.
# To reset the sample schema, replace everything with
# two dots ('..' - without quotes).

Blockchain
-
previous_hash PK string
timestamp float 
signature_of_transactions string
index bigint

Wallet
-
public_key PK string FK - Peer_nodes.public_key

Transactions
-
signature string pk FK - Blockchain.signature_of_transactions
sender string FK >- Wallet.public_key
recipient string FK >- Wallet.public_key
amount float

Peer_nodes
-
id string pk
public_key string
