import React, { useState, useEffect } from 'react';
import axios from 'axios';
import styles from '../css/Comandas.module.css';
import mesaImage from '../imagens/mesa.png';
import TabelaImprimivel from './TabelaImprimivel';

function Comandas() {
  const [modalOpen, setModalOpen] = useState(false);
  const [selectedMesa, setSelectedMesa] = useState(null);
  const [mesas, setMesas] = useState([]);
  const [conta, setConta] = useState([]);
  const [tabelaHtml, setTabelaHtml] = useState('');
  const [cnpj, setCnpj] = useState('');
  const [email, setEmail] = useState('');
  const [endereco, setEndereco] = useState('');
  const [nomeEst, setNomeEst] = useState('');
  const [nomeFunc, setNomeFunc] = useState('');
  const [data, setData] = useState('');

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

  useEffect(() => {
    const fetchInformacoesEst = async () => {
      try {
        const response = await axios.get('/informacoesEst');
        const data = response.data;
        setNomeEst(data.nomeEst);
        setCnpj(data.cnpj);
        setEmail(data.email);
        setEndereco(data.endereco);
        setNomeFunc(data.nomeFunc);
        const dataAtual = new Date();
        const options = {
          year: 'numeric',
          month: 'numeric',
          day: 'numeric',
          hour: 'numeric',
          minute: 'numeric'
        };
        setData(dataAtual.toLocaleDateString('pt-BR', options));
      } catch (error) {
        console.error('Erro ao obter informações do estabelecimento:', error);
      }
    };

    fetchInformacoesEst();
  }, []);

  useEffect(() => {
    const buildTable = () => {
      const tabelaHtml2 = `
        <table className=${styles.table}>
          <thead className=${styles.colun}>
            <tr>
              <td colSpan="4" className=${styles.titlecolun}>
                <span style="float: left;"><strong>Estabelecimento: </strong> ${nomeEst}</span>
                <span style="float: right;"><strong>CNPJ: </strong> ${cnpj}</span>
              </td>
            </tr>
            <tr>
              <td colSpan="4" className=${styles.titlecolun}>
                <span style="float: left;"><strong>Endereço: </strong>${endereco}</span>
              </td>
            </tr>
            <tr>
              <td colSpan="4" className=${styles.titlecolun}>
                <span style="float: left;"><strong>Email: </strong>${email}</span>
              </td>
            </tr>
            <tr>
              <td colSpan="4" className=${styles.titlecolun}>
                <span style="float: left;"><strong>Operador: </strong> ${nomeFunc}</span>
                <span style="float: right;"><strong>Data: </strong> ${data}</span>
              </td>
            </tr>
            <tr '-separator'}>
              <td colSpan="4" style="height: 10px; border-bottom: 1px solid #847663;"></td>
            </tr>
            <tr>
              <th className=${styles.titlecolun}>Prato</th>
              <th className=${styles.titlecolun}>Quantidade</th>
              <th className=${styles.titlecolun}>Valor unitário</th>
              <th className=${styles.titlecolun}>Valor total</th>
            </tr>
          </thead>
          <tbody className=${styles.tbody}>
            ${conta.slice(0, -1).map((item, index) => {
              return (`
                <tr key=${index}>
                  <td style="text-align: center; vertical-align: middle;">${item.nome}</td>
                  <td style="text-align: center; vertical-align: middle;">${item.quantidade}</td>
                  <td style="text-align: center; vertical-align: middle;">${item.valorun ? `R$${item.valorun}` : ''}</td>
                  <td style="text-align: center; vertical-align: middle;">${item.valorprod ? `R$${item.valorprod}` : ''}</td>
                </tr>
                ${index !== conta.length - 2 ? `
                  <tr key=${index + '-separator'}>
                    <td colSpan="4" style="height: 10px; border-bottom: 1px solid #847663;"></td>
                  </tr>
                ` : ''}
              `);
            }).join('')}
            <tr>
              <td className=${styles.titlecolun}><strong></strong></td>
              <td colSpan="2"></td>
              <td className=${styles.textodireita}><strong>Total: ${conta.length > 0 ? `R$${conta[conta.length - 1].valorTotal}` : 'R$0.00'}</strong></td>
            </tr>
            <tr '-separator'}>
              <td colSpan="4" style="height: 10px; border-bottom: 1px solid #847663;"></td>
            </tr>
            <tr>
              <td colSpan="4" className=${styles.titlecolun}>
                <span style="float: left;"><strong>OBS: Este recibo não comprova o pagamento.</strong></span>
              </td>
            </tr>
          </tbody>
        </table>
      `;
      setTabelaHtml(tabelaHtml2);
    };

    buildTable();
  }, [conta, nomeEst, cnpj, endereco, email, nomeFunc, data]);

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
          </div>
        </div>
      )}
    </div>
  );
}

export default Comandas;
