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
    id           integer primary key,
    name         varchar(255),
    price        numeric,
    type         varchar(25),
    pack_item_id integer default null,
    pack_size    integer default null,
    foreign key (pack_item_id) references Items (id)
);

insert into Items(id, name, price, type, pack_item_id, pack_size)
values (0, 'Beer', 3.99, 'SINGLE', null, null),
       (1, '6x Beer Pack', null, 'PACK', 0, 6),
       (2, 'Cheese', 2.99, 'SINGLE', null, null),
       (3, 'Bread', 1.45, 'SINGLE', null, null);

CREATE TABLE
    Receipt_items
(
    receipt_id integer,
    item_id    integer,
    quantity   integer default 1,
    foreign key (receipt_id) references Receipts (_id),
    foreign key (item_id) references Items (id)
);
