import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import {ViewPageBuilderComponent} from './view-page-builder.component';


const routes: Routes = [
						{ path : '' ,redirectTo : '/',pathMatch:'full'},
						{ path: 'page/:slug', component: ViewPageBuilderComponent, data: { editorType: 1 } },
            			{ path: 'campaign/:slug', component: ViewPageBuilderComponent, data: { editorType: 2 } },
                       ];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class ViewPageBuilderRoutingModule { }
