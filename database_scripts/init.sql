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
    id        integer primary key,
    name      varchar(255),
    price     numeric,
    parent_id integer default null,
    foreign key (parent_id) references Items (id)
);

insert into Items(id, name, price, parent_id)
values (0, 'Beer', 3.99, null),
       (1, '6x Beer Pack', 14.99, 0),
       (2, 'Cheese', 2.99, null),
       (3, 'Bread', 1.45, null);

CREATE TABLE
    Receipt_items
(
    receipt_id integer,
    item_id    integer,
    quantity   integer default 1,
    foreign key (receipt_id) references Receipts (_id),
    foreign key (item_id) references Items (id)
);
