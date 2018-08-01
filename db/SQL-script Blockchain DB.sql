-- Exported from QuickDBD: https://www.quickdatatabasediagrams.com/
-- Link to schema: https://app.quickdatabasediagrams.com/#/schema/apBRv5MRjUGiOmAYVWdSug
-- NOTE! If you have used non-SQL datatypes in your design, you will have to change these here.

-- Modify this code to update the DB schema diagram.
-- To reset the sample schema, replace everything with
-- two dots ('..' - without quotes).

CREATE TABLE `blockchain` (
    `index` INTEGER  NOT NULL ,
    `previous_hash` TEXT  NOT NULL ,
    `hash_of_txs` TEXT ,
    `proof` INTEGER ,
    `timestamp` REAL  NOT NULL ,
    PRIMARY KEY (
        `index`
    ),
    FOREIGN KEY (`index`) REFERENCES transactions(block)
);

CREATE TABLE `wallet` (
    `public_key` text NOT NULL ,
    `node_id` text not NULL ,
    PRIMARY KEY (
        `public_key`
    )
);

CREATE TABLE `transactions` (
    `sender` TEXT  NOT NULL ,
    `recipient` TEXT  NOT NULL ,
    `amount` REAL  NOT NULL ,
    `signature` TEXT  NOT NULL ,
    `mined` INTEGER NOT NULL,
    `block` text,
    `time` REAL,
    PRIMARY KEY (
        `signature`
    ),
    FOREIGN KEY (sender) REFERENCES `wallet` (`public_key`),
    FOREIGN KEY (recipient) REFERENCES `wallet` (`public_key`),
    FOREIGN KEY (block) REFERENCES `blockchain` (`index`)
);

CREATE TABLE `peer_nodes` (
    `id` TEXT  NOT NULL ,
    PRIMARY KEY (
        `id`
    ),
    FOREIGN KEY (`id`) REFERENCES wallet(`node_id`)
);
