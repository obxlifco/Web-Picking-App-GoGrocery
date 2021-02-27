import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ProductpromotionsComponent } from './productpromotions.component';

describe('ProductpromotionsComponent', () => {
  let component: ProductpromotionsComponent;
  let fixture: ComponentFixture<ProductpromotionsComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ ProductpromotionsComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(ProductpromotionsComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
