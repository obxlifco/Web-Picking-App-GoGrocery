import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ProductpromotionmodelComponent } from './productpromotionmodel.component';

describe('ProductpromotionmodelComponent', () => {
  let component: ProductpromotionmodelComponent;
  let fixture: ComponentFixture<ProductpromotionmodelComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ ProductpromotionmodelComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(ProductpromotionmodelComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
