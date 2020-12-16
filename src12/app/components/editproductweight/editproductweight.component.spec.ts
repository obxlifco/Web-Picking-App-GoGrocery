import { ComponentFixture, TestBed } from '@angular/core/testing';

import { EditproductweightComponent } from './editproductweight.component';

describe('EditproductweightComponent', () => {
  let component: EditproductweightComponent;
  let fixture: ComponentFixture<EditproductweightComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ EditproductweightComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(EditproductweightComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
