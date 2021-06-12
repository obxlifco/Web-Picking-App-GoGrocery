import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import { CategoryBannerComponent } from './category-banner.component';
import { CategoryBannerAddeditComponent } from './category-banner-addedit.component';

const routes: Routes = [
  { path: '', component: CategoryBannerComponent },
  { path: 'add', component: CategoryBannerAddeditComponent },
  { path: 'edit/:id', component: CategoryBannerAddeditComponent },
];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class CategoryBannerRoutingModule { }
