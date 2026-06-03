import { test, expect, APIRequestContext, request } from '@playwright/test';

const BASE_URL = 'http://localhost:3000'; // Change as needed

// Helper to generate random emails/usernames for uniqueness
function randomString(length: number) {
  const chars = 'abcdefghijklmnopqrstuvwxyz0123456789';
  let result = '';
  for (let i = 0; i < length; i++) {
    result += chars.charAt(Math.floor(Math.random() * chars.length));
  }
  return result;
}

test.describe('User Registration API', () => {
  let apiContext: APIRequestContext;

  test.beforeAll(async ({ playwright }) => {
    apiContext = await request.newContext({
      baseURL: BASE_URL,
      extraHTTPHeaders: {
        'Content-Type': 'application/json',
      },
    });
  });

  test.afterAll(async () => {
    await apiContext.dispose();
  });

  test('Positive Test Case: Successful User Registration', async () => {
    const user = {
      username: `user_${randomString(8)}`,
      email: `user_${randomString(8)}@test.com`,
      password: 'Password123!',
    };

    const response = await apiContext.post('/register', { data: user });
    expect(response.status()).toBe(201);

    const body = await response.json();
    expect(body).toHaveProperty('userId');
    expect(body).toHaveProperty('message');
    expect(typeof body.userId).toBe('string');
    expect(typeof body.message).toBe('string');
  });

  test('Negative Test Case: User Registration with Existing Email', async () => {
    const email = `existing_${randomString(8)}@test.com`;
    const user1 = {
      username: `user1_${randomString(8)}`,
      email,
      password: 'Password123!',
    };
    const user2 = {
      username: `user2_${randomString(8)}`,
      email,
      password: 'Password123!',
    };

    // Register first user
    const response1 = await apiContext.post('/register', { data: user1 });
    expect(response1.status()).toBe(201);

    // Attempt to register second user with same email
    const response2 = await apiContext.post('/register', { data: user2 });
    expect(response2.status()).toBe(409);

    const body = await response2.json();
    // Should not reveal if email is registered
    expect(typeof body.message).toBe('string');
    expect(body.message.toLowerCase()).not.toContain('registered');
    expect(body.message.toLowerCase()).not.toContain(email.toLowerCase());
  });

  test('Negative Test Case: User Registration with Missing Required Fields', async () => {
    const user = {
      // username is missing
      email: `missing_${randomString(8)}@test.com`,
      password: 'Password123!',
    };

    const response = await apiContext.post('/register', { data: user });
    expect(response.status()).toBe(400);

    const body = await response.json();
    expect(typeof body.error).toBe('string');
    expect(body.error.toLowerCase()).toContain('username');
    expect(body.error.toLowerCase()).toContain('missing');
  });

  test('Negative Test Case: User Registration with Invalid Email Format', async () => {
    const user = {
      username: `invalidemail_${randomString(8)}`,
      email: 'invalid-email-format',
      password: 'Password123!',
    };

    const response = await apiContext.post('/register', { data: user });
    expect(response.status()).toBe(400);

    const body = await response.json();
    expect(typeof body.error).toBe('string');
    expect(body.error.toLowerCase()).toContain('email');
    expect(body.error.toLowerCase()).toContain('invalid');
  });

  test('Edge Test Case: User Registration with Minimum Length Password', async () => {
    const user = {
      username: `minpass_${randomString(8)}`,
      email: `minpass_${randomString(8)}@test.com`,
      password: '123', // less than 6 chars
    };

    const response = await apiContext.post('/register', { data: user });
    expect(response.status()).toBe(400);

    const body = await response.json();
    expect(typeof body.error).toBe('string');
    expect(body.error.toLowerCase()).toContain('password');
    expect(body.error.toLowerCase()).toContain('length');
  });

  test('Edge Test Case: User Registration with Maximum Length Username', async () => {
    const maxUsername = randomString(50);
    const user = {
      username: maxUsername,
      email: `maxuser_${randomString(8)}@test.com`,
      password: 'Password123!',
    };

    const response = await apiContext.post('/register', { data: user });
    expect(response.status()).toBe(201);

    const body = await response.json();
    expect(body).toHaveProperty('userId');
    expect(body).toHaveProperty('message');
    expect(typeof body.userId).toBe('string');
    expect(typeof body.message).toBe('string');
  });

  test('Concurrency Test Case: Simultaneous User Registration Requests', async () => {
    const users = Array.from({ length: 5 }).map((_, i) => ({
      username: `concurrent_${i}_${randomString(8)}`,
      email: `concurrent_${i}_${randomString(8)}@test.com`,
      password: 'Password123!',
    }));

    const responses = await Promise.all(
      users.map(user => apiContext.post('/register', { data: user }))
    );

    for (const response of responses) {
      expect(response.status()).toBe(201);
      const body = await response.json();
      expect(body).toHaveProperty('userId');
      expect(body).toHaveProperty('message');
    }
  });

  test('Security Test Case: User Registration with SQL Injection', async () => {
    const user = {
      username: "'; DROP TABLE users; --",
      email: `sqlinj_${randomString(8)}@test.com`,
      password: 'Password123!',
    };

    const response = await apiContext.post('/register', { data: user });
    expect(response.status()).toBe(400);

    const body = await response.json();
    expect(typeof body.error).toBe('string');
    expect(body.error.toLowerCase()).toContain('invalid');
    // Optionally, check that error does not contain SQL error details
    expect(body.error.toLowerCase()).not.toContain('sql');
    expect(body.error.toLowerCase()).not.toContain('syntax');
  });

  test('Error Handling Test Case: User Registration with Invalid Data Types', async () => {
    const user = {
      username: 12345, // invalid type
      email: `datatype_${randomString(8)}@test.com`,
      password: 'Password123!',
    };

    const response = await apiContext.post('/register', { data: user });
    expect(response.status()).toBe(400);

    const body = await response.json();
    expect(typeof body.error).toBe('string');
    expect(body.error.toLowerCase()).toContain('username');
    expect(body.error.toLowerCase()).toContain('string');
    expect(body.error.toLowerCase()).toContain('type');
  });

  test('Data Integrity Test Case: User Registration Data Persistence', async () => {
    // Register user
    const user = {
      username: `dataintegrity_${randomString(8)}`,
      email: `dataintegrity_${randomString(8)}@test.com`,
      password: 'Password123!',
    };

    const registerResponse = await apiContext.post('/register', { data: user });
    expect(registerResponse.status()).toBe(201);

    const registerBody = await registerResponse.json();
    expect(registerBody).toHaveProperty('userId');
    const userId = registerBody.userId;

    // Retrieve user details (assuming /users/:id endpoint exists)
    const getResponse = await apiContext.get(`/users/${userId}`);
    expect(getResponse.status()).toBe(200);

    const userBody = await getResponse.json();
    expect(userBody).toHaveProperty('username', user.username);
    expect(userBody).toHaveProperty('email', user.email);
    // Password should not be returned for security reasons
    expect(userBody).not.toHaveProperty('password');
  });
});