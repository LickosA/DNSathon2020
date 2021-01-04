import { Routes } from '@angular/router';
import { DocComponent } from './doc/doc.component';
import { GalleryComponent } from './gallery/gallery.component';
import { HomeComponent } from './home/home.component';
import { TestComponent } from './test/test.component';

export const routes: Routes = [
    {path: '', component: HomeComponent},
    {path: 'audit/:dn', component: TestComponent, },
    {path : 'doc', component: DocComponent},
    {path: 'contact', component: GalleryComponent}
]