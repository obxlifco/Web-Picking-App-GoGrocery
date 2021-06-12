import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';

import { GroupComponent }  from '../../employee/group/employee.group.component';
import { GroupAddEditComponent }  from '../../employee/group/employee.group.addedit.component';

const routes: Routes = [
  {
    path:'',
    component:GroupComponent
  },
  {
    path:'add',
    component:GroupAddEditComponent
  },
  {
    path:'edit/:id',
    component:GroupAddEditComponent
  },
];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class GroupRoutingModule { }
