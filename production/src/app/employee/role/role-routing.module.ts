import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';

import { RoleComponent }  from '../../employee/role/employee.role.component';
import { RoleAddEditComponent }  from '../../employee/role/employee.role.addedit.component';

const routes: Routes = [
  {
    path:'',
    component:RoleComponent
  },
  {
    path:'add',
    component:RoleAddEditComponent
  },
  {
    path:'edit/:id',
    component:RoleAddEditComponent
  },
];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class RoleRoutingModule { }
