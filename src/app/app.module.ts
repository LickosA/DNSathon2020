import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';
import { DnsAuditService } from './apiProviders/dns-audit.service';

import { AppComponent } from './app.component';
import { TestComponent } from './test/test.component';
import { HomeComponent } from './home/home.component';
import { DocComponent } from './doc/doc.component';
import { GalleryComponent } from './gallery/gallery.component';
import { BaseComponent } from './base/base.component';
import { HttpClientModule } from '@angular/common/http';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';
import { RouterModule } from '@angular/router';
import { routes } from './app-routing.module';

@NgModule({
  declarations: [
    AppComponent,
    TestComponent,
    HomeComponent,
    DocComponent,
    GalleryComponent,
    BaseComponent
  ],
  imports: [
    // BrowserAnimationsModule,
    ReactiveFormsModule,
    BrowserModule,
    HttpClientModule,
    FormsModule,
    RouterModule.forRoot(routes)
  ],
  providers: [DnsAuditService],
  bootstrap: [AppComponent]
})
export class AppModule { }
