import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ImagemagnifyComponent } from './imagemagnify.component';

describe('ImagemagnifyComponent', () => {
  let component: ImagemagnifyComponent;
  let fixture: ComponentFixture<ImagemagnifyComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ ImagemagnifyComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(ImagemagnifyComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
