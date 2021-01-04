import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';

@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.css']
})
export class HomeComponent implements OnInit {
  dn: string;
  slideIndex = 0;
  navs = document.getElementsByClassName('nav-item');

  constructor(private _router: Router) { }

  ngOnInit(): void {
    this.showSlides(this.slideIndex);
  }

  currentSlide(n): void {
    this.showSlides(n);
  }

  showSlides(n): void {
    var i;
    var slides = document.getElementsByClassName('slider-item');
    var dots = document.getElementsByClassName('owl-dot');

    if (n > slides.length) {
      this.slideIndex = 1;
    }

    if (n < 1) {
      this.slideIndex = slides.length;
    }

    for (i = 0; i < slides.length; i++) {
        // @ts-ignore
        slides[i].style.display = 'none';
    }

    for (i = 0; i < dots.length; i++) {
        dots[i].className = dots[i].className.replace(' active', '');
    }

    // @ts-ignore
    slides[n].style.display = 'block';
    // @ts-ignore
    slides[n].style.transform = 'translateZ(0px) translateY(0%)';

    dots[n].className += ' active';

    if (n === 0) {
      setTimeout( () => {
        this.showSlides(1);
      }, 8000);
    }

    else if (n === 1) {
      setTimeout( () => {
        this.showSlides(0);
      }, 8000);
    }
  }

  check(): void {
    this._router.navigate(['/audit/', this.dn]);
  }

}
