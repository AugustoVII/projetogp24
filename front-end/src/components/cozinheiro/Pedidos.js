import React, { useState, useEffect } from 'react';
import styles from '../css/Pedidos.module.css';
import axios from 'axios';
import Modal from '../modal/Modal'
function Pedidos() {
  const [selectedPedido, setSelectedPedido] = useState(' ');
  const [showModal, setShowModal] = useState(false);
  const [pedidos, setPedidos] = useState([]);
  const [mensagem, setMensagem] = useState('');

  const handleConfirm = () => {
    // Lógica de confirmação, por exemplo, atualizando o status do pedido
    const formData = {
      pedidoId: selectedPedido, // Envie apenas o ID do pedido
    };

    axios.post('/marcarpedido', formData)
      .then(response => {
        // Verifique o status da resposta para determinar se a requisição foi bem-sucedida
        if (response.status === 200) { // Verifique o status 200 para sucesso
          setMensagem('Pedido marcado como concluído!');
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

    // Função para buscar pedidos a cada 5 segundos
    const interval = setInterval(fetchPedidos, 3000); // Consulta a cada 5 segundos (ajuste conforme necessário)

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
      <ul className={styles.listaMesas}>
        {pedidos.map((pedido, index) => (
          <li key={index} className={styles.liMesa}>
            <span className={styles.numeroMesa}>Mesa {pedido.mesa} pedido {pedido.pedido}</span>
            <div className={styles.tablediv} onClick={() => handlePedidoClick(pedido.pedido)}>
              <table className={styles.table}>
                <thead className={styles.colun}>
                  <tr>
                    <th className={styles.titlecolun}>Quantidade</th>
                    <th className={styles.titlecolun}>Prato</th>
                  </tr>
                </thead>
                <tbody className={styles.tbody}>
                  <tr className={styles.tr} key={pedido.pedido}>
                    <td className={styles.quant}>{pedido.quantidade}</td>
                    <td className={styles.prato}>{pedido.prato}</td>
                  </tr>
                </tbody>
              </table>
            </div>
          </li>
        ))}
      </ul>
      {showModal &&(
        <div><Modal show={showModal} handleClose={handleClose} handleConfirm={handleConfirm}>
        <p className={styles.titulo}>Tem certeza que deseja confirmar o pedido?</p>
      </Modal></div>
      )}
      
    </div>
  );
}

export default Pedidos;
