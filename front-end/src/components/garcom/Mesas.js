import { useState, useEffect } from 'react';
import styles from '../css/Mesas.module.css';
import mesaImage from '../imagens/mesa.png';

function Mesas() {
  const [modalOpen, setModalOpen] = useState(false);
  const [selectedMesa, setSelectedMesa] = useState(null);
  const [quantidade, setQuantidade] = useState('');
  const [pratos, setPratos] = useState([]);
  const [pratoSelecionado, setPratoSelecionado] = useState('');
  const [pedidos, setPedidos] = useState([]);
  const [mesas,setMesas] = useState([]);

  useEffect(() => {
    fetch('/mesas')
      .then(response => response.json())
      .then(data => {
        setMesas(data.mesas);
      })
      .catch(error => {
        console.error('Erro ao obter dados:', error);
      });
  }, []);

  useEffect(() => {
    const fetchProdutos = async () => {
      try {
        const response = await fetch('/produto');
        if (!response.ok) {
          throw new Error('Falha ao obter produtos');
        }
        const data = await response.json();
        const nomes = data.produtos.map(produto => produto.nome);
        setPratos(nomes);
      } catch (error) {
        console.error('Erro ao obter nomes dos produtos:', error);
      }
    };
    fetchProdutos();
  }, []);

  const handleVoltar = () => {
    setPratoSelecionado('');
    setQuantidade('');
    setSelectedMesa('');
    setPedidos([]);
    setModalOpen(false);
    
  };

  const handleMesaClick = (mesa) => {
    setSelectedMesa(mesa);
    setModalOpen(true);
  };

  const handleAddPedido = (e) => {
  e.preventDefault();
  if (pratoSelecionado && quantidade && selectedMesa) {
    const novoPedido = {
      mesaId: selectedMesa.id,
      prato: pratoSelecionado,
      quantidade: quantidade
    };
    setPedidos([...pedidos, novoPedido]);
    setPratoSelecionado('');
    setQuantidade('');
  } else {
    if (!pratoSelecionado) {
      alert("Por favor, selecione um prato.");
    } else if (!quantidade) {
      alert("Por favor, insira a quantidade.");
    }
  }
};

const handleEnviarPedidos = async (e) => {
  e.preventDefault();
  try {
    const response = await fetch('/pedido', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ pedidos })
    });
    
    if (!response.ok) {
      throw new Error('Erro ao enviar pedidos');
    }
    
    alert("Pedidos enviados com sucesso.");
    setPedidos([]);
    setModalOpen(false);
  } catch (error) {
    console.error('Erro ao enviar pedidos:', error);
  }
};

  const mudaPrato = (event) => {
    setPratoSelecionado(event.target.value);
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
              {mesa.status === "ocupada" && <div className={styles.bolinhaVermelha}></div>}
              {mesa.status === "livre" && <div className={styles.bolinhaVerde}></div>}
            </div>
            <span className={styles.numeroMesa}>Mesa {mesa.numero}</span>
          </li>
        ))}
      </ul>
      {modalOpen && (
        <div className={styles.fullScreenModal}>
          <div className={styles.modalContent}>
            <span className={styles.close} onClick={() => setModalOpen(false)}>&times;</span>
            <h2>Adicionar Pedido à Mesa {selectedMesa.numero}</h2>
            <form className={styles.form} >
              <div className={styles.inputcontainer}>
                <div className={styles.inputgroup}>
                  <p className={styles.namegroup}>Quantidade:</p>
                  <input type="number"
                    className={styles.input} 
                    placeholder="Digite a quantidade" 
                    value={quantidade} 
                    onChange={(e) => {
                    const inputQuantidade = parseInt(e.target.value);
                    if (!isNaN(inputQuantidade) && inputQuantidade >= 0) {
                      setQuantidade(inputQuantidade);
                      }
                      }}
                  required
                  />
                </div>
                <div className={styles.inputgroup}>
                  <p className={styles.namegroup}>Pedido:</p>
                  <select className ={styles.inputlist} value={pratoSelecionado} onChange={mudaPrato}>
                    <option value="">Selecione um prato</option>
                    {pratos.map((prato, index) => (
                      <option key={index} value={prato}>{prato}</option>
                    ))}
                  </select>
                </div>
              </div>
              <button className={styles.bottomgroup} onClick={() => handleVoltar()}>Cancelar</button>
              {pedidos.length > 0 && (
                <button className={styles.bottomgroup} onClick={handleEnviarPedidos}>Enviar</button>
              )}
              <button className={styles.bottomgroup} onClick={handleAddPedido}>Adicionar </button>
            </form>
          </div>
        </div>
      )}
    </div>
  );
}

export default Mesas;
