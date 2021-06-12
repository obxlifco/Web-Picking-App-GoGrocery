import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import {DetailsComponent} from './details.component';
import { HomeRouterResolverService } from '../../global/service/router-resolver.service';


const routes: Routes = [
	{path : '',component : DetailsComponent, resolve: { data: HomeRouterResolverService }}
];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class DetailsRoutingModule { }
