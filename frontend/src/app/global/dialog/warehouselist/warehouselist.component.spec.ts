import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { WarehouselistComponent } from './warehouselist.component';

describe('WarehouselistComponent', () => {
  let component: WarehouselistComponent;
  let fixture: ComponentFixture<WarehouselistComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ WarehouselistComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(WarehouselistComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
