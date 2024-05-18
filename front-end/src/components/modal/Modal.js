import React from 'react';
import styles from '../css/Modal.module.css';

const Modal = ({ show, handleClose, handleConfirm, children }) => {
  const showHideClassName = show ? "modal display-block" : "modal display-none";

  return (
    <div className={styles.fullScreenModal}>
      <section className={styles.modalContent}>
        {children}
        <button className={styles.bottomgroup} onClick={handleClose}>Cancelar</button>
        <button className={styles.bottomgroup} onClick={handleConfirm}>Confirmar</button>
      </section>
    </div>
  );
};

export default Modal;
