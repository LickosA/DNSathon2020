import { Component, OnInit } from '@angular/core';

@Component({
  selector: 'app-gallery',
  templateUrl: './gallery.component.html',
  styleUrls: ['./gallery.component.css']
})
export class GalleryComponent implements OnInit {
  navs = document.getElementsByClassName('nav-item');

  constructor() { }

  ngOnInit(): void {
    // for (const i in this.navs) {
    //   this.navs[i].classList.remove('active');
    //   this.navs[3].classList.add('active');
    // }
  }

}
