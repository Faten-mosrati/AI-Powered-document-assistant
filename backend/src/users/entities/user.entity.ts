import { Column, CreateDateColumn, Entity, PrimaryGeneratedColumn, UpdateDateColumn } from "typeorm";


@Entity()
export class User {

@PrimaryGeneratedColumn()
id: number;


@Column()
firstName: string;

@Column()
lastName: string;       

@Column({unique: true, length: 255})
email: string;

@Column()
password: string;

@Column({ default: false })
isActive: boolean;

@CreateDateColumn()
createdAt: Date;

@UpdateDateColumn()
updatedAt: Date;
}
