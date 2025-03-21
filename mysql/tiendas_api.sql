USE dev_testeos;

##Creaciones de las tablas en nuestra base de datos de dev
CREATE TABLE productos(
	id_producto int not null auto_increment,
    nombre varchar(80) not null, 
    descripcion varchar(99) not null,
    precio float not null default 0,
    id_categoria int not null,
    #stock int not null default 0,
    tiempo_disponible float not null default 0,
    id_proveedor int not null,
    primary key(id_producto)
    );

#ALTER TABLE productos DROP COLUMN stock;
select * from detalles_compras;
CREATE TABLE detalles_compras(
	id_producto int not null,
    id_pedido int not null,
	id_cliente int not null,
	cantidad float not null default 0,
    unidad varchar(10) not null default 1,
    precio float not null,
    metodo_Pago varchar(10) not null,
    primary key(id_producto, id_pedido),
    foreign key(id_producto) references productos(id_producto)
    );
    
CREATE TABLE compras(
	id_pedido int not null,
    id_cliente int not null,
    fecha_pedido timestamp default current_timestamp,
    importe_total float not null default 1,
    primary key(id_pedido)
	);

CREATE TABLE categorias(
	id_categoria int not null,
    nombre varchar(80) not null,
    primary key(id_categoria)
    );


CREATE TABLE proveedores(
	id_proveedor int not null,
    nombre varchar(50) not null,
    contacto varchar(80),
    direccion varchar(80) not null,
    primary key(id_proveedor)
    );

CREATE TABLE clientes(
	id_cliente int not null,
    nombre_compelto varchar(80) not null,
    email varchar(80) not null,
    telefono int not null,
    direccion varchar(80),
    primary key(id_cliente)
    );
    

CREATE TABLE stock(
	id_producto int not null,
    fecha_stock timestamp default current_timestamp,
    cantidad float not null default 0,
    unidad varchar(15),
    primary key(id_producto)
    );

##Inserts y selects para validar ##

INSERT INTO productos(nombre, descripcion, precio, id_categoria, tiempo_disponible, id_proveedor)
VALUES("Camiseta", "Camiseta básica blanca", 5.00, 0001, 8, 0001), ("Mesa", "Mesa básica madera blanca", 20.20, 0002, 40, 0002),
("Blusa", "Blusa básica blanca", 11.00, 0001, 15, 0001), ("Pantalón vaquero", "Pantalón vaquero básico azul", 17.00, 0001, 15, 0001);
    
SELECT * FROM productos;
--

INSERT INTO detalles_compras(id_producto,id_pedido,cantidad,unidad,precio,metodo_Pago)
VALUES(1,20242070, 3, "unidades", 8, "Efectivo"), (2, 20247776, 1, "unidades", 20.20, "Tarjeta"),
(3,20242070, 2, "unidades", 11.0, "Efectivo"), (4,20242478 , 2, "unidades", 17, "Tarjeta");


select * from detalles_compras;
ALTER TABLE detalles_compras ADD COLUMN id_cliente int not null;
#SET SQL_SAFE_UPDATES = 0;
UPDATE detalles_compras SET id_cliente = 29083583 WHERE id_pedido = 20242070;
UPDATE detalles_compras SET id_cliente = 86705541 WHERE id_pedido = 20247776;
UPDATE detalles_compras SET id_cliente = 15629191 WHERE id_pedido = 20242478;

INSERT INTO compras(id_pedido,id_cliente,fecha_pedido,importe_total) 
VALUES (20242070, 29083583, '2025-03-10',46), (20247776, 86705541, '2025-02-22',20.20), (20242478, 15629191, '2025-01-05',34);



INSERT INTO categorias(id_categoria, nombre) VALUES (01, "Ropa"),(02,"Muebles");

INSERT INTO proveedores(id_proveedor,nombre,contacto,direccion)
VALUES (0001,"Interno", "textiles_ibericas@iberica.es", "Aquí"), (0002, "Ikea", "ikea@ikea.com", "Calle Ikea, 14");


INSERT INTO clientes(id_cliente,nombre_compelto,email,telefono,direccion)
VALUES(29083583, "Manuel Alén", "manuelalen@protonmail.com","699999999", "Calle Manolito"),
(86705541, "Cristiano Ronal", "cristiano@bicho.com", "777777777", "Calle El Bicho"),
(15629191, "Benito Antonio Martinez Ocasio", "badbunny@benito.com", "999999999", "Avenida Benito");

UPDATE clientes SET nombre_completo = "Cristiano Ronaldo" WHERE id_cliente = 86705541;

INSERT INTO stock(id_producto,fecha_stock,cantidad,unidad) VALUES(1,'2025-01-01',1000,"Unidades"),
(2, '2025-01-02',300,"Unidades"), (3,'2025-01-02', 1300, "Unidades"), (4,'2025-01-04',500,"Unidades");


## probadura de este trigger
DELIMITER $$

CREATE TRIGGER trg_act_stock_compras
AFTER INSERT ON detalles_compras
FOR EACH ROW
BEGIN
    -- ✅ 1. Actualizar stock
    UPDATE stock
    SET 
        fecha_stock = CURRENT_TIMESTAMP,
        cantidad = cantidad - NEW.cantidad
    WHERE id_producto = NEW.id_producto;

    -- ✅ 2. Insertar o actualizar en compras
    INSERT INTO compras (id_pedido, id_cliente, fecha_pedido, importe_total)
    VALUES (NEW.id_pedido, NEW.id_cliente, CURRENT_TIMESTAMP, 
            (SELECT SUM(precio) FROM detalles_compras WHERE id_pedido = NEW.id_pedido))
    ON DUPLICATE KEY UPDATE 
        importe_total = (SELECT SUM(precio) FROM detalles_compras WHERE id_pedido = NEW.id_pedido),
        fecha_pedido = CURRENT_TIMESTAMP;
END $$

DELIMITER ;


## Nuevo insert de testeo del triger ##
INSERT INTO detalles_compras (id_producto,id_pedido,id_cliente, cantidad,unidad,precio,metodo_Pago)
VALUES(1,20252017,86705541, 1, "unidades", 8, "Efectivo");

