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

    // Função para buscar pedidos a cada 5 segundos
    const interval = setInterval(fetchPedidos, 3000); // Consulta a cada 5 segundos (ajuste conforme necessário)

    // Limpa o intervalo quando o componente é desmontado
    return () => clearInterval(interval);
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
