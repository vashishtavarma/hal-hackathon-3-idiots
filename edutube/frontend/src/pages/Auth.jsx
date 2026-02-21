import { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { login } from '../api/client';
import { useAuth } from '../context/AuthContext';
import styles from './Auth.module.css';

export default function Auth() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [submitting, setSubmitting] = useState(false);
  const { login: setAuth } = useAuth();
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setSubmitting(true);
    try {
      const data = await login({ email, password });
      setAuth(data.access_token, data.user);
      navigate('/', { replace: true });
    } catch (err) {
      setError(err.message || 'Sign in failed');
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <div className={styles.page}>
      <div className={styles.card}>
        <div className={styles.cardLogo}>
          <span className={styles.cardLogoIcon} aria-hidden>◇</span>
          <span className={styles.cardLogoText}>Thrive Learn</span>
        </div>
        <h1 className={styles.title}>Sign in to your account</h1>
        <form onSubmit={handleSubmit} className={styles.form}>
          {error && <p className={styles.error}>{error}</p>}
          <label htmlFor="email">Your email</label>
          <input
            id="email"
            type="email"
            placeholder="abc@email.com"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            required
            autoComplete="email"
          />
          <label htmlFor="password">Password</label>
          <input
            id="password"
            type="password"
            placeholder="••••••••"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
            autoComplete="current-password"
          />
          <button type="submit" className={styles.submit} disabled={submitting}>
            {submitting ? 'Signing in…' : 'Sign in'}
          </button>
        </form>
        <p className={styles.footer}>
          Don't have an account? <Link to="/signup">Sign up here</Link>
        </p>
        <div className={styles.social}>
          <a href="https://facebook.com" target="_blank" rel="noopener noreferrer">Facebook</a>
          <a href="https://twitter.com" target="_blank" rel="noopener noreferrer">Twitter</a>
          <a href="https://github.com" target="_blank" rel="noopener noreferrer">Github</a>
          <a href="https://dribbble.com" target="_blank" rel="noopener noreferrer">Dribbble</a>
        </div>
      </div>
    </div>
  );
}
