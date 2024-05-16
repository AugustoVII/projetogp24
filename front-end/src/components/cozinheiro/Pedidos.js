import React, { useState, useEffect } from 'react';
import styles from '../css/Pedidos.module.css';
import axios from 'axios';

function Pedidos() {
  const [selectedPedido, setSelectedPedido] = useState(null);
  const [pedidos, setPedidos] = useState([]);
  const [mensagem, setMensagem] = useState('');

  useEffect(() => {
    const fetchPedidos = async () => {
      try {
        const response = await axios.get('/pedido');
        setPedidos(response.data);
      } catch (error) {
        console.error('Erro ao buscar os pedidos:', error);
      }
    };

    fetchPedidos();
  }, []);

  const handlePedidoClick = (pedido) => {
    if (window.confirm('Confirmar pedido')) {
      setSelectedPedido(pedido);

      // Envie o pedido marcado como concluído
      const formData = {
        pedidoId: pedido, // Envie apenas o ID do pedido
      };

      axios.post('/marcarpedido', formData)
        .then(response => {
          if (response.data.success) {
            setMensagem('Pedido marcado como concluído!');
            // Atualize a lista de pedidos após o sucesso
            setPedidos(prevPedidos => prevPedidos.filter(p => p.pedido !== pedido));
          } else {
            setMensagem('Erro ao marcar o pedido como concluído. Tente novamente.');
          }
        })
        .catch(error => {
          console.error('Erro ao enviar:', error);
          setMensagem('Erro ao enviar. Tente novamente.');
        });
    }
  };

  return (
    <div className={styles.divPrinc}>
      <h1>Pedidos</h1>
      <p>{mensagem}</p>
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
    </div>
  );
}

export default Pedidos;
