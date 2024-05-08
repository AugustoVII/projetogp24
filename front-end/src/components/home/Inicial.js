import React from 'react';
import styles from '../css/Home.module.css';
import logo from '../imagens/aberto.png';

function Inicial() {
  return (
    <div className={styles.container}>
      <img src={logo} alt="Logo do site" className={styles.logo} />
    </div>
  );
}

export default Inicial;
