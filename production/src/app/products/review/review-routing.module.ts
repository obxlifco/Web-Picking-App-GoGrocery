import { NgModule, Component } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';

import { ReviewComponent }  from '../../products/review/products.review.component';
import { ReviewAddeditComponent } from '../../products/review/review.addedit.component';
const routes: Routes = [
  { path:'', component:ReviewComponent},
  { path: 'add', component: ReviewAddeditComponent },
  { path: 'edit/:id', component: ReviewAddeditComponent },
];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class ReviewRoutingModule { }
