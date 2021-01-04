import { Component, OnInit } from '@angular/core';

@Component({
  selector: 'app-doc',
  templateUrl: './doc.component.html',
  styleUrls: ['./doc.component.css']
})
export class DocComponent implements OnInit {
  navs = document.getElementsByClassName('nav-item');

  constructor() { }

  ngOnInit(): void {
    // for (const i in this.navs) {
    //   this.navs[i].classList.remove('active');
    //   this.navs[2].classList.add('active');
    // }
  }

}
