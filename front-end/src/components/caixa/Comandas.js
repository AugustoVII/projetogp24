import React, { useState, useEffect } from 'react';
import axios from 'axios';
import styles from '../css/Comandas.module.css';
import mesaImage from '../imagens/mesa.png';
import TabelaImprimivel from './TabelaImprimivel'; // Importe o componente TabelaImprimivel aqui

function Comandas() {
  const [modalOpen, setModalOpen] = useState(false);
  const [selectedMesa, setSelectedMesa] = useState(null);
  const [mesas,setMesas] = useState([]);
  const [conta,setConta] = useState([]);
  const [tabelaHtml, setTabelaHtml] = useState(``);

  useEffect(() => {
    const fetchMesas = async () => {
      try {
        const response = await axios.get('/mesasocupadas');
        setMesas(response.data.mesas);
      } catch (error) {
        console.error('Erro ao buscar as mesas:', error);
      }
    };

    // Função para buscar pedidos e mesas a cada 5 segundos
    const interval = setInterval(() => {
      fetchMesas();
    }, 3000); // Consulta a cada 5 segundos (ajuste conforme necessário)

    // Limpa o intervalo quando o componente é desmontado
    return () => clearInterval(interval);
  }, []);

  const handleVoltar = () => {
    setConta('');
    setSelectedMesa('');
    setModalOpen(false);
  };

  const handleMesaClick = async (mesa) => {
    try {
      const response = await axios.get(`/contamesa/${mesa.id}`);
      setConta(response.data); 
      setSelectedMesa(mesa);
      setModalOpen(true);
  
      if (response.data.length === 0) {
        console.log('A conta está vazia.');
        return;
      }
  
      const tabelaHtml2 = `
        <table className=${styles.table}>
          <thead className=${styles.colun}>
            <tr>
              <th className=${styles.titlecolun}>Prato</th>
              <th className=${styles.titlecolun}>Quantidade</th>
              <th className=${styles.titlecolun}>Valor unitario</th>
              <th className=${styles.titlecolun}>Valor total</th>
            </tr>
          </thead>
          <tbody>
            ${response.data.slice(0, -1).map((item, index) => {
              return (`
                <tr key=${index}>
                  <td style="text-align: center; vertical-align: middle;">${item.nome}</td>
                  <td style="text-align: center; vertical-align: middle;">${item.quantidade}</td>
                  <td style="text-align: center; vertical-align: middle;">${item.valorun ? `R$${item.valorun}` : ''}</td>
                  <td style="text-align: center; vertical-align: middle;">${item.valorprod ? `R$${item.valorprod}` : ''}</td>
                </tr>
                ${index !== response.data.length - 2 ? `
                  <tr key=${index + '-separator'}>
                    <td colSpan="4" style="height: 10px; border-bottom: 1px solid #847663;"></td>
                  </tr>
                ` : ''}
              `);
            }).join('')}
            <tr>
              <td className=${styles.titlecolun}><strong></strong></td>
              <td colSpan="2"></td>
              <td className=${styles.textodireita}><strong>Total: ${response.data.length > 0 ? `R$${response.data[response.data.length - 1].valorTotal}` : 'R$0.00'}</strong></td>
            </tr>
          </tbody>
        </table>
      `;
      setTabelaHtml(tabelaHtml2);
    } catch (error) {
      console.error('Erro ao selecionar a mesa:', error);
    }
  };
  

  const handleFechaComanda = () => {
    console.log(selectedMesa);
    setModalOpen(false);
  };


return (
    <div className={styles.divPrinc}>
      <h1>Mesas</h1>
      <ul className={styles.listaMesas}>
        {mesas.map((mesa, index) => (
          <li key={index} className={styles.liMesa}>
            <div onClick={() => handleMesaClick(mesa)} className={styles.imagemMesaContainer}>
              <img
                src={mesaImage}
                className={styles.imagemMesa}
                alt={`Mesa ${mesa.numero}`}
              />
            </div>
            <span className={styles.numeroMesa}>Mesa {mesa.numero}</span>
          </li>
          
        ))}
      </ul>
      {modalOpen && (
        <div className={styles.fullScreenModal}>
          <div className={styles.modalContent}>
            <span className={styles.close} onClick={() => setModalOpen(false)}>&times;</span>
            <h2>Comanda mesa {selectedMesa.numero}</h2>
            <div className={styles.imprimir}><TabelaImprimivel tabelaHtml={tabelaHtml} /></div>
            
            <div className={styles.tablediv}>
            <table className={styles.table}>
              <thead className={styles.colun}>
                <tr>
                  <th className={styles.titlecolun}>Prato</th>
                  <th className={styles.titlecolun}>Quantidade</th>
                  <th className={styles.titlecolun}>Valor unitario</th>
                  <th className={styles.titlecolun}>Valor total</th>
                </tr>
              </thead>
              <tbody className={styles.tbody}>
              {conta.map((item, index) => (
              <React.Fragment key={index}>
                <tr>
                  <td>{item.nome}</td>
                  <td>{item.quantidade}</td>
                  <td>{item.valorun ? `R$${item.valorun}` : ''}</td>
                  <td>{item.valorprod ? `R$${item.valorprod}` : ''}</td>
                </tr>
                {index !== conta.length - 1 && (
                <tr key={`${index}-separator`}>
                  <td colSpan="4" style={{ height: '10px', borderBottom: '1px solid #847663' }}></td>
                </tr>
              )}
              </React.Fragment>
            ))}
            
            <tr>
            <td colSpan="3" style={{ textAlign: 'right' }}><strong>Total:</strong></td>
            <td style={{ textAlign: 'right' }}><strong>{conta.length > 0 ? `R$${conta[conta.length - 1].valorTotal}` : 'R$0.00'}</strong></td>
          </tr>
              </tbody>
            </table>
          </div>
              <button className={styles.bottomgroup} onClick={() => handleVoltar()}>Cancelar</button>
              
              <button className={styles.bottomgroup} onClick={handleFechaComanda}>Fechar</button>
            <div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

export default Comandas;
