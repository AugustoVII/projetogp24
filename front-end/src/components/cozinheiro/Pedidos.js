import React, { useState, useEffect } from 'react';
import styles from '../css/Pedidos.module.css';
import axios from 'axios';
import Modal from '../modal/Modal';

function Pedidos() {
  const [selectedPedido, setSelectedPedido] = useState(null);
  const [showModal, setShowModal] = useState(false);
  const [pedidos, setPedidos] = useState([]);
  const [mensagem, setMensagem] = useState('');

  const handleConfirm = () => {
    // Verifique se selectedPedido está definido
    if (!selectedPedido) return;

    // Lógica de confirmação, por exemplo, atualizando o status do pedido
    const formData = {
      pedidoId: selectedPedido.pedido, // Envie o ID do pedido
      idpedidoproduto: selectedPedido.idpedidoproduto, // Envie o ID do pedidoproduto
    };

    axios.post('/marcarpedido', formData)
      .then(response => {
        // Verifique o status da resposta para determinar se a requisição foi bem-sucedida
        if (response.status === 200) { // Verifique o status 200 para sucesso
          setMensagem('Pedido marcado como concluído!');
          // Atualize a lista de pedidos removendo o pedido concluído baseado no idpedidoproduto
          setPedidos(prevPedidos => prevPedidos.filter(p => p.idpedidoproduto !== selectedPedido.idpedidoproduto));
        } else {
          setMensagem('Erro ao marcar o pedido como concluído. Tente novamente.');
        }
      })
      .catch(error => {
        console.error('Erro ao enviar:', error);
        setMensagem('Erro ao enviar. Tente novamente.');
      });
    setShowModal(false);
  };

  useEffect(() => {
    const fetchPedidos = async () => {
      try {
        const response = await axios.get('/pedido');
        setPedidos(response.data);
      } catch (error) {
        console.error('Erro ao buscar os pedidos:', error);
      }
    };

    // Função para buscar pedidos a cada 3 segundos
    const interval = setInterval(fetchPedidos, 3000); // Consulta a cada 3 segundos (ajuste conforme necessário)

    // Limpa o intervalo quando o componente é desmontado
    return () => clearInterval(interval);
  }, []);

  const handlePedidoClick = (pedido) => {
    setSelectedPedido(pedido);
    setShowModal(true);
  };

  const handleClose = () => {
    setShowModal(false);
  };

  return (
    <div className={styles.divPrinc}>
      <h1>Pedidos</h1>
      <p>{mensagem}</p>
      <ul className={styles.listaMesas}>
        {pedidos.map((pedido, index) => (
          <li key={index} className={styles.liMesa}>
            <span className={styles.numeroMesa}>Mesa {pedido.mesa} pedido {pedido.pedido}</span>
            <div className={styles.tablediv} onClick={() => handlePedidoClick(pedido)}>
              <table className={styles.table}>
                <thead className={styles.colun}>
                  <tr>
                    <th className={styles.titlecolun}>Quantidade</th>
                    <th className={styles.titlecolun}>Prato</th>
                  </tr>
                </thead>
                <tbody className={styles.tbody}>
                  <tr key={pedido.pedido}>
                    <td>{pedido.quantidade}</td>
                    <td>{pedido.prato}</td>
                  </tr>
                </tbody>
              </table>
            </div>
          </li>
        ))}
      </ul>
      {showModal && (
        <Modal show={showModal} handleClose={handleClose} handleConfirm={handleConfirm}>
          <p className={styles.titulo}>Tem certeza que deseja confirmar o pedido?</p>
        </Modal>
      )}
    </div>
  );
}

export default Pedidos;
