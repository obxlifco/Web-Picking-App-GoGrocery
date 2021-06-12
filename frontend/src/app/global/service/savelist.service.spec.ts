import { TestBed } from '@angular/core/testing';

import { SavelistService } from './savelist.service';

describe('SavelistService', () => {
  beforeEach(() => TestBed.configureTestingModule({}));

  it('should be created', () => {
    const service: SavelistService = TestBed.get(SavelistService);
    expect(service).toBeTruthy();
  });
});
