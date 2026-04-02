<?php

namespace Tests\Feature;

use App\Models\User;
use Illuminate\Foundation\Testing\RefreshDatabase;
use Tests\TestCase;

class AuthTest extends TestCase
{
    use RefreshDatabase;

    public function test_register_exitoso(): void
    {
        $response = $this->postJson('/api/auth/register', [
            'email'                 => 'test@example.com',
            'password'              => 'Password123*',
            'password_confirmation' => 'Password123*',
            'role'                  => 'student',
        ]);

        $response->assertStatus(201)
                 ->assertJsonStructure([
                     'success', 'token', 'user' => ['id', 'email', 'role', 'status']
                 ]);
    }

    public function test_register_falla_email_duplicado(): void
    {
        User::factory()->create(['email' => 'test@example.com']);

        $response = $this->postJson('/api/auth/register', [
            'email'                 => 'test@example.com',
            'password'              => 'Password123*',
            'password_confirmation' => 'Password123*',
            'role'                  => 'student',
        ]);

        $response->assertStatus(422);
    }

    public function test_register_falla_role_invalido(): void
    {
        $response = $this->postJson('/api/auth/register', [
            'email'                 => 'test2@example.com',
            'password'              => 'Password123*',
            'password_confirmation' => 'Password123*',
            'role'                  => 'admin',
        ]);

        $response->assertStatus(422);
    }

    public function test_register_falla_passwords_no_coinciden(): void
    {
        $response = $this->postJson('/api/auth/register', [
            'email'                 => 'test3@example.com',
            'password'              => 'Password123*',
            'password_confirmation' => 'OtraPassword123*',
            'role'                  => 'student',
        ]);

        $response->assertStatus(422);
    }

    public function test_login_exitoso(): void
    {
        User::factory()->create([
            'email'    => 'login@example.com',
            'password' => bcrypt('Password123*'),
            'role'     => 'student',
            'status'   => 'active',
        ]);

        $response = $this->postJson('/api/auth/login', [
            'email'    => 'login@example.com',
            'password' => 'Password123*',
        ]);

        $response->assertStatus(200)
                 ->assertJsonStructure(['success', 'token', 'user']);
    }

    public function test_login_falla_credenciales_incorrectas(): void
    {
        $response = $this->postJson('/api/auth/login', [
            'email'    => 'noexiste@example.com',
            'password' => 'WrongPassword',
        ]);

        $response->assertStatus(401);
    }

    public function test_login_falla_cuenta_inactiva(): void
    {
        User::factory()->create([
            'email'    => 'inactivo@example.com',
            'password' => bcrypt('Password123*'),
            'role'     => 'student',
            'status'   => 'inactive',
        ]);

        $response = $this->postJson('/api/auth/login', [
            'email'    => 'inactivo@example.com',
            'password' => 'Password123*',
        ]);

        $response->assertStatus(403);
    }

    public function test_forgot_password_email_existente(): void
    {
        User::factory()->create(['email' => 'forgot@example.com']);

        $response = $this->postJson('/api/auth/forgot-password', [
            'email' => 'forgot@example.com',
        ]);

        $response->assertStatus(200)
                 ->assertJson(['success' => true]);
    }

    public function test_forgot_password_email_no_existente(): void
    {
        $response = $this->postJson('/api/auth/forgot-password', [
            'email' => 'noexiste@example.com',
        ]);

        $response->assertStatus(422);
    }

    public function test_me_requiere_autenticacion(): void
    {
        $response = $this->getJson('/api/auth/me');
        $response->assertStatus(401);
    }

    public function test_logout_requiere_autenticacion(): void
    {
        $response = $this->postJson('/api/auth/logout');
        $response->assertStatus(401);
    }
}