import { useAuth } from '../context/AuthContext';
import { Link } from 'react-router-dom';
import styles from './Profile.module.css';

export default function Profile() {
  const { user } = useAuth();

  if (!user) {
    return (
      <div className={styles.profile}>
        <p>Please <Link to="/auth">sign in</Link> to view your profile.</p>
      </div>
    );
  }

  return (
    <div className={styles.profile}>
      <h1 className={styles.heading}>Profile</h1>
      <div className={styles.card}>
        <p><strong>Name</strong> {user.name}</p>
        <p><strong>Email</strong> {user.email}</p>
        <p className={styles.muted}>
          Member since {new Date(user.created_at).toLocaleDateString()}
        </p>
      </div>
    </div>
  );
}
