-- Tabla para almacenar direcciones de entrega
CREATE TABLE direccion_entrega (
    id_direccion INT AUTO_INCREMENT PRIMARY KEY,
    calle VARCHAR(255),
    ciudad VARCHAR(100),
    estado VARCHAR(100),
    codigo_postal VARCHAR(20)
);

-- Tabla para almacenar los pedidos
CREATE TABLE pedido (
    id_pedido INT AUTO_INCREMENT PRIMARY KEY,
    fecha_pedido DATE,
    direccion_entrega_id INT,
    FOREIGN KEY (direccion_entrega_id) REFERENCES direccion_entrega(id_direccion)
);

-- Tabla para almacenar la información de los clientes
CREATE TABLE cliente (
    id_cliente INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100),
    apellido VARCHAR(100),
    email VARCHAR(100),
    cedula VARCHAR(20),
    telefono VARCHAR(20)
);

-- Tabla para almacenar los carritos de compra
CREATE TABLE carrito_compra (
    id_carrito INT AUTO_INCREMENT PRIMARY KEY,
    cliente_id INT,
    pedido_id INT,
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (pedido_id) REFERENCES pedido(id_pedido),
    FOREIGN KEY (cliente_id) REFERENCES cliente(id_cliente)
);

-- Tabla para almacenar las categorías de empleados
CREATE TABLE categoria_empleado (
    id_categoria INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100),
    descripcion TEXT
);

-- Tabla para almacenar la información de los empleados
CREATE TABLE empleado (
    id_empleado INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100),
    apellido VARCHAR(100),
    cargo VARCHAR(100),
    salario DECIMAL(10, 2),
    fecha_contrato DATE,
    categoria_id INT,
    FOREIGN KEY (categoria_id) REFERENCES categoria_empleado(id_categoria)
);

-- Tabla para almacenar las promociones
CREATE TABLE promociones (
    id_promocion INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100),
    descripcion TEXT,
    fecha_inicio DATE,
    fecha_fin DATE,
    descuento DECIMAL(5, 2)
);

-- Tabla para almacenar las facturas
CREATE TABLE factura (
    id_factura INT AUTO_INCREMENT PRIMARY KEY,
    fecha_factura DATE,
    total DECIMAL(10, 2),
    cliente_id INT,
    empleado_id INT,
    promociones_id INT,
    FOREIGN KEY (promociones_id) REFERENCES promociones(id_promocion),
    FOREIGN KEY (empleado_id) REFERENCES empleado(id_empleado),
    FOREIGN KEY (cliente_id) REFERENCES cliente(id_cliente)
);

-- Tabla para almacenar los contratos de los empleados
CREATE TABLE contrato (
    id_contrato INT AUTO_INCREMENT PRIMARY KEY,
    empleado_id INT,
    tipo_contrato VARCHAR(100),
    fecha_inicio DATE,
    fecha_fin DATE,
    salario DECIMAL(10, 2),
    FOREIGN KEY (empleado_id) REFERENCES empleado(id_empleado)
);

-- Tabla para almacenar los métodos de pago
CREATE TABLE metodo_pago (
    id_metodo INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100),
    descripcion TEXT
);

-- Tabla para almacenar las categorías de productos
CREATE TABLE categoria_producto (
    id_categoria INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100),
    descripcion TEXT
);

-- Tabla para almacenar los proveedores
CREATE TABLE proveedor (
    id_proveedor INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100),
    contacto VARCHAR(100),
    telefono VARCHAR(20),
    email VARCHAR(100)
);

-- Tabla para almacenar la información de los productos
CREATE TABLE producto (
    id_producto INT AUTO_INCREMENT PRIMARY KEY,
    proveedor_id INT,
    nombre VARCHAR(100),
    descripcion TEXT,
    precio DECIMAL(10, 2),
    categoria_id INT,
    FOREIGN KEY (categoria_id) REFERENCES categoria_producto(id_categoria),
    FOREIGN KEY (proveedor_id) REFERENCES proveedor(id_proveedor)
);

-- Tabla para almacenar los detalles de las facturas
CREATE TABLE detalle_factura (
    id_detalle INT AUTO_INCREMENT PRIMARY KEY,
    factura_id INT,
    producto_id INT,
    metodo_id INT,
    cantidad INT,
    precio_unitario DECIMAL(10, 2),
    FOREIGN KEY (factura_id) REFERENCES factura(id_factura),
    FOREIGN KEY (producto_id) REFERENCES producto(id_producto),
    FOREIGN KEY (metodo_id) REFERENCES metodo_pago(id_metodo)
);

-- Tabla para almacenar los pasillos de la tienda
CREATE TABLE pasillo (
    id_pasillo INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100)
);

-- Tabla para almacenar los detalles de los productos
CREATE TABLE detalle_producto (
    id_detalle_producto INT AUTO_INCREMENT PRIMARY KEY,
    producto_id INT,
    pasillo_id INT,
    fecha_ingreso DATE,
    cantidad INT,
    precio_compra DECIMAL(10, 2),
    FOREIGN KEY (producto_id) REFERENCES producto(id_producto),
    FOREIGN KEY (pasillo_id) REFERENCES pasillo(id_pasillo)
);

-- Tabla para almacenar las bodegas
CREATE TABLE bodega (
    id_bodega INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100),
    direccion VARCHAR(255),
    ciudad VARCHAR(100),
    estado VARCHAR(100),
    codigo_postal VARCHAR(20)
);

-- Tabla para almacenar los productos en la bodega
CREATE TABLE producto_bodega (
    id_producto_bodega INT AUTO_INCREMENT PRIMARY KEY,
    producto_id INT,
    bodega_id INT,
    cantidad INT,
    FOREIGN KEY (producto_id) REFERENCES producto(id_producto),
    FOREIGN KEY (bodega_id) REFERENCES bodega(id_bodega)
);


