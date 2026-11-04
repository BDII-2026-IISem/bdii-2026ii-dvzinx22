import { Injectable, inject } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { environment } from '../../../environments/environment';
import { User, Role, Resource, RoleUser, ResourceRole } from '../models/rbac.model';

@Injectable({
  providedIn: 'root',
})
export class RbacService {
  private readonly http = inject(HttpClient);
  private readonly apiUrl = environment.apiUrl;

  // Usuarios
  getUsers(): Observable<User[]> {
    return this.http.get<User[]>(`${this.apiUrl}/users/`);
  }

  createUser(user: Partial<User>): Observable<User> {
    return this.http.post<User>(`${this.apiUrl}/users/`, user);
  }

  updateUser(id: number, user: Partial<User>): Observable<User> {
    return this.http.put<User>(`${this.apiUrl}/users/${id}/`, user);
  }

  deleteUser(id: number): Observable<void> {
    return this.http.delete<void>(`${this.apiUrl}/users/${id}/`);
  }

  // Roles
  getRoles(): Observable<Role[]> {
    return this.http.get<Role[]>(`${this.apiUrl}/roles/`);
  }

  createRole(role: Partial<Role>): Observable<Role> {
    return this.http.post<Role>(`${this.apiUrl}/roles/`, role);
  }

  updateRole(id: number, role: Partial<Role>): Observable<Role> {
    return this.http.put<Role>(`${this.apiUrl}/roles/${id}/`, role);
  }

  deleteRole(id: number): Observable<void> {
    return this.http.delete<void>(`${this.apiUrl}/roles/${id}/`);
  }

  // Recursos HTTP
  getResources(): Observable<Resource[]> {
    return this.http.get<Resource[]>(`${this.apiUrl}/resources/`);
  }

  createResource(resource: Partial<Resource>): Observable<Resource> {
    return this.http.post<Resource>(`${this.apiUrl}/resources/`, resource);
  }

  deleteResource(id: number): Observable<void> {
    return this.http.delete<void>(`${this.apiUrl}/resources/${id}/`);
  }

  // Asignaciones Role-User
  getRoleUsers(): Observable<RoleUser[]> {
    return this.http.get<RoleUser[]>(`${this.apiUrl}/role-users/`);
  }

  assignRoleToUser(payload: { user: number; role: number; status?: string }): Observable<RoleUser> {
    return this.http.post<RoleUser>(`${this.apiUrl}/role-users/`, {
      ...payload,
      status: payload.status || 'active',
    });
  }

  // Concesiones Resource-Role
  getResourceRoles(): Observable<ResourceRole[]> {
    return this.http.get<ResourceRole[]>(`${this.apiUrl}/resource-roles/`);
  }

  assignResourceToRole(payload: { role: number; resource: number; status?: string }): Observable<ResourceRole> {
    return this.http.post<ResourceRole>(`${this.apiUrl}/resource-roles/`, {
      ...payload,
      status: payload.status || 'active',
    });
  }
}

