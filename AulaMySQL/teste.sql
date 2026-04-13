-- ==========================================
-- SCRIPT DE CRIAÇÃO DE BANCO DE DADOS TESTE
-- ==========================================

-- Remove o banco se ele já existir para evitar conflitos
DROP DATABASE IF EXISTS teste_db;

-- Cria o banco de dados
CREATE DATABASE teste_db;
USE teste_db;

-- Criar a tabela de Clientes
CREATE TABLE clientes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE,
    data_cadastro DATE
);

-- Criar a tabela de Pedidos (Relacionada aos Clientes)
CREATE TABLE pedidos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    cliente_id INT,
    produto VARCHAR(100),
    valor DECIMAL(10, 2),
    data_pedido TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (cliente_id) REFERENCES clientes(id) ON DELETE CASCADE
);

-- Inserindo Clientes para teste
INSERT INTO clientes (nome, email, data_cadastro) VALUES
('Ana Silva', 'ana@email.com', '2024-01-15'),
('Bruno Costa', 'bruno@email.com', '2024-02-20'),
('Carla Souza', 'carla@email.com', '2024-03-05');

-- Inserindo Pedidos para teste
INSERT INTO pedidos (cliente_id, produto, valor) VALUES
(1, 'Notebook', 3500.00),
(1, 'Mouse Gamer', 150.00),
(2, 'Monitor 24"', 900.00),
(3, 'Teclado Mecânico', 250.00);

-- Query de verificação rápida
SELECT 
    c.nome AS Cliente, 
    p.produto AS Produto, 
    p.valor AS Preco
FROM clientes c
JOIN pedidos p ON c.id = p.cliente_id;