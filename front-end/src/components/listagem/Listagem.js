import { useState, useEffect } from 'react';
import styles from '../css/Listagem.module.css';
import Modal from '../modal/Modal';
function Listagem() {
  const [usuarios, setUsuarios] = useState([]);
  const [showModal, setShowModal] = useState(false);
  const [usuarioSelecionado, setUsuarioSelecionado] = useState(null);
  
  const handleConfirm = () => {
    fetch(`/excluirusuario/${usuarioSelecionado}`, {
      method: 'GET',
    })
    .then(response => {
      if (response.ok) {
        console.log('Usuário excluído com sucesso.');
        window.location.reload();
      } else {
        console.error('Falha ao excluir usuário.');
      }
    })
    .catch(error => {
      console.error('Erro ao excluir usuário:', error);
    });
    setShowModal(false);
  };

  useEffect(() => {
    fetch('/listausuario')
      .then(response => response.json())
      .then(data => {
        setUsuarios(data.usuarios);
      })
      .catch(error => {
        console.error('Erro ao obter dados:', error);
      });
  }, []); 

  const handleClose = () => {
    setShowModal(false);
  };
  const excluirUsuario = (id) => {
    // Define o usuário selecionado para exclusão
    setUsuarioSelecionado(id);
    // Abre o modal de confirmação
    setShowModal(true);
  };
  
  return (
    <div className={styles.Main}>
      <div className={styles.div}>
        <h1>Listagem de funcionários</h1>
        <div className={styles.tablediv}>
          <table className={styles.table}>
            <thead className={styles.colun}>
              <tr>
                <th className={styles.titlecolun}>Nome</th>
                <th className={styles.titlecolun}>Tipo</th>
                <th className={styles.titlecolun}>Ação</th>
              </tr>
            </thead>
            <tbody className={styles.tbody}>
              {usuarios.map((usuario, index) => (
                <tr key={index}>
                  <td>{usuario.nome}</td>
                  <td>{usuario.tipo}</td>
                  <td>
                    <button className={styles.buttonGroup} onClick={excluirUsuario}>
                      Editar
                    </button>{' '}
                    <button className={styles.buttonGroup} onClick={() => excluirUsuario(usuario.id)}>
                      Excluir
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
      {showModal &&(
        <div><Modal show={showModal} handleClose={handleClose} handleConfirm={handleConfirm}>
        <p className={styles.titulo}>Tem certeza que deseja excluir o usuario?</p>
      </Modal></div>
      )}
    </div>
  );
}

export default Listagem;
