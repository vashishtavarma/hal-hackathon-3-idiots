import { Link } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import styles from './Home.module.css';

export default function Home() {
  const { user } = useAuth();

  return (
    <div className={styles.home}>
      <h1 className={styles.heading}>
        {user ? `Hi, ${user.name}` : 'Welcome to Thrive Learn'}
      </h1>
      <p className={styles.lead}>
        Transform YouTube into a focused, interactive learning environment: reduce distractions
        and add notes, AI assistance, quizzes, and collaboration.
      </p>
      {!user && (
        <p className={styles.hint}>
          <Link to="/auth">Sign in</Link> or <Link to="/signup">create an account</Link> to save your progress and notes.
        </p>
      )}
    </div>
  );
}
