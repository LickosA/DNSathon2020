import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';

@Injectable({
  providedIn: 'root'
})
export class DnsAuditService {

  base = 'https://dnsathon2020-api.herokuapp.com/api/audit/';

  constructor(private httpClient: HttpClient) { }

  makeAudit(dn) {
    let header = new HttpHeaders({
      'Access-Control-Allow-Origin': '*',
      'Access-Control-Allow-Methods': '*'
    });

    return this.httpClient.get(this.base + dn, {headers: header});
  }
}
