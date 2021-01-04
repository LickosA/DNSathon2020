import { HttpHeaders } from '@angular/common/http';
import { Component, OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { DnsAuditService } from '../apiProviders/dns-audit.service';

@Component({
  selector: 'app-test',
  templateUrl: './test.component.html',
  styleUrls: ['./test.component.css']
})
export class TestComponent implements OnInit {
  loading = false;
  showResults = false;
  dn: string;
  dn_checked: string;
  navs = document.getElementsByClassName('nav-item');
  auditResults: any;
  auditResults_loc = [];
  // auditResults = {
  //   EXIST: true,
  //   INFO_IPV6: false,
  //   INFO_MX: {
  //     exist: true,
  //     number: 2,
  //     list: [
  //       '10 mx2.hostinger.fr.',
  //       '5 mx1.hostinger.fr.'
  //     ]
  //   },
  //   INFO_NS: {
  //     list: [
  //       'ns2.dns-parking.com.',
  //       'ns1.dns-parking.com.'
  //     ],
  //     ns_location: {
  //       'ns1.dns-parking.com.': 'United States, Chicago',
  //       'ns2.dns-parking.com.': 'United States, Chicago',
  //       'ns3.dns-parking.com.': 'United Stes, Chicago',
  //       'ns4.dns-parking.com.': 'United Stes, Chicago'
  //     },
  //     number: 2,
  //     same_asn: true
  //   },
  //   INFO_SOA: true,
  //   PERFORMANCE_DNSTIME: '0.39 ms',
  //   PERFORMANCE_EDNS: true,
  //   SEC_DNSSEC: {
  //     dns_key: false,
  //     ds: false,
  //     exist: false
  //   },
  //   SEC_SSL: true
  // };

  constructor(private Audit: DnsAuditService,
              private _activatedRoute: ActivatedRoute) { }

  ngOnInit(): void {

    // document.getElementById('mod_btn').click();
    // console.log(this.auditResults);
    // for (const i in this.auditResults.INFO_NS.ns_location) {
    //   if (!this.auditResults_loc.includes(this.auditResults.INFO_NS.ns_location[i])) {
    //     this.auditResults_loc.push(this.auditResults.INFO_NS.ns_location[i]);
    //   }
    // }

    this.dn = this._activatedRoute.snapshot.paramMap.get('dn');
    this.dn_checked = this.dn;

    if (this.dn.length > 3) {
      this.makeAudit();
    } else {
      this.dn = undefined;
    }

  }

  makeAudit() {
    // reinitialisation des permettant le trie et l'affichage de la réponse
    this.auditResults = [];
    this.auditResults_loc = [];
    
    // stop affichage et lancement loading
    this.showResults = false;
    this.loading = true;
    this.Audit.makeAudit(this.dn).subscribe(
      res => {
        this.auditResults = res;

        if (!this.auditResults.EXIST) {
          document.getElementById('mod_btn').click();
          this.loading = false;
        }

        else {
          // fait le trie pour qu'il n'y ai pas les même location affichés
          for (const i in this.auditResults.INFO_NS.ns_location) {
            if (!this.auditResults_loc.includes(this.auditResults.INFO_NS.ns_location[i])) {
              this.auditResults_loc.push(this.auditResults.INFO_NS.ns_location[i]);
            }
          }

          // stop loading et lancement affichage
          this.showResults = true;
          this.loading = false;
        }

      },
      err => {
        console.log(err);
        this.loading = false;
      }
    );
  }

}
