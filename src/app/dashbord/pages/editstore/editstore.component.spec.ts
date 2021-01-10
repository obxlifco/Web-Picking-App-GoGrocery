import { ComponentFixture, TestBed } from '@angular/core/testing';

import { EditstoreComponent } from './editstore.component';

describe('EditstoreComponent', () => {
  let component: EditstoreComponent;
  let fixture: ComponentFixture<EditstoreComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ EditstoreComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(EditstoreComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
