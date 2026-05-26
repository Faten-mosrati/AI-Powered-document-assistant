import { ConflictException, Injectable } from '@nestjs/common';
import { Repository } from 'typeorm';
import { User } from './entities/user.entity';
import { InjectRepository } from '@nestjs/typeorm';
import * as bcrypt from 'bcryptjs';

@Injectable()
export class UsersService {
   constructor(
    @InjectRepository(User)
    private readonly repo: Repository<User>,
  ) {}

   async findById(id: number): Promise<User | null> {
     return this.repo.findOne({ where: { id } });
  }

    async create(firstName: string, lastName: string, email: string, password: string): Promise<User> {
      const exists = await this.repo.findOne({
        where: [{ email }],
      });
      if (exists) {
        throw new ConflictException(
          exists.email=== email? 'Email taken' : 'Email taken',
        );
      }
  
      const hashed = await bcrypt.hash(password, 12);
      const user = this.repo.create({ firstName,lastName, email, password: hashed })
    return this.repo.save(user);
  }
 
  async findByEmail(email: string): Promise<User | null> {
    return this.repo.findOne({ where: { email } });
  }

  async validateCredentials(email: string, password: string): Promise<User | null>
  {

    const user = await this.findByEmail(email);
    if (!user) return null;
    const valid = await bcrypt.compare(password, user.password);
    return valid ? user : null;
  }
  }
  

