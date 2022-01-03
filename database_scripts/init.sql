CREATE TABLE
    Receipts
(
    _id       integer primary key,
    closed    tinyint default 0,
    open_date varchar(50)
);

CREATE TABLE
    Items
(
    _id               integer primary key,
    name              varchar(255),
    price             numeric,
    discount          numeric,
    quantity          integer,
    reference_item_id integer default null,
    foreign key (reference_item_id) references Items (_id)
);

CREATE TABLE
    Receipt_items
(
    receipt_id integer,
    item_id    integer,
    quantity   integer default 1,
    foreign key (receipt_id) references Receipts (_id),
    foreign key (item_id) references Items (_id)
);
