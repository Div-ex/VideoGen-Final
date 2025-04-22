// src/__tests__/RegisterPage.test.js
jest.mock('react-router-dom', () => ({
  useNavigate: () => jest.fn(),
}));

import { render, screen, fireEvent } from '@testing-library/react';
import RegisterPage from '../RegisterPage';
import { MemoryRouter } from 'react-router-dom';

beforeEach(() => {
  global.fetch = jest.fn(() =>
    Promise.resolve({ ok: true })
  );
});

test('registers user successfully', async () => {
  render(
    <MemoryRouter>
      <RegisterPage />
    </MemoryRouter>
  );

  fireEvent.change(screen.getByPlaceholderText(/username/i), {
    target: { value: 'testuser' },
  });

  fireEvent.change(screen.getByPlaceholderText(/password/i), {
    target: { value: 'testpass' },
  });

  fireEvent.click(screen.getByText(/register/i));

  expect(global.fetch).toHaveBeenCalledWith(
    expect.stringContaining('/register'),
    expect.objectContaining({
      method: 'POST',
      body: JSON.stringify({ username: 'testuser', password: 'testpass' }),
    })
  );
});