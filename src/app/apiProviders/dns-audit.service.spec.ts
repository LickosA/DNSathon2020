import { TestBed } from '@angular/core/testing';

import { DnsAuditService } from './dns-audit.service';

describe('DnsAuditService', () => {
  let service: DnsAuditService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(DnsAuditService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
