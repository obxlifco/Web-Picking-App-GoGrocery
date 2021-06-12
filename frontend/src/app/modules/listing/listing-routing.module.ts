import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import {ListingComponent} from './listing.component';
import { HomeRouterResolverService } from '../../global/service/router-resolver.service';

const routes: Routes = [
  {path : ':slug',component:ListingComponent,resolve: { data: HomeRouterResolverService }},
  {path : 'brand/:slug',component:ListingComponent},
];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class ListingRoutingModule { }
