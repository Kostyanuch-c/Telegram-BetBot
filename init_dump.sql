PGDMP     
    6            	    |            telegram_betbot %   14.13 (Ubuntu 14.13-0ubuntu0.22.04.1)    15.3 :    :           0    0    ENCODING    ENCODING        SET client_encoding = 'UTF8';
                      false            ;           0    0 
   STDSTRINGS 
   STDSTRINGS     (   SET standard_conforming_strings = 'on';
                      false            <           0    0 
   SEARCHPATH 
   SEARCHPATH     8   SELECT pg_catalog.set_config('search_path', '', false);
                      false            =           1262    151236    telegram_betbot    DATABASE     w   CREATE DATABASE telegram_betbot WITH TEMPLATE = template0 ENCODING = 'UTF8' LOCALE_PROVIDER = libc LOCALE = 'C.UTF-8';
    DROP DATABASE telegram_betbot;
                postgres    false            >           0    0    DATABASE telegram_betbot    ACL     1   GRANT ALL ON DATABASE telegram_betbot TO portal;
                   postgres    false    3389                        2615    2200    public    SCHEMA        CREATE SCHEMA public;
    DROP SCHEMA public;
                postgres    false            ?           0    0    SCHEMA public    COMMENT     6   COMMENT ON SCHEMA public IS 'standard public schema';
                   postgres    false    4            @           0    0    SCHEMA public    ACL     Q   REVOKE USAGE ON SCHEMA public FROM PUBLIC;
GRANT ALL ON SCHEMA public TO PUBLIC;
                   postgres    false    4            I           1247    167657    role    TYPE     E   CREATE TYPE public.role AS ENUM (
    'USER',
    'ADMINISTRATOR'
);
    DROP TYPE public.role;
       public          portal    false    4            �            1259    167629    alembic_version    TABLE     X   CREATE TABLE public.alembic_version (
    version_num character varying(32) NOT NULL
);
 #   DROP TABLE public.alembic_version;
       public         heap    portal    false    4            �            1259    167635 
   bookmakers    TABLE     a   CREATE TABLE public.bookmakers (
    name character varying NOT NULL,
    id integer NOT NULL
);
    DROP TABLE public.bookmakers;
       public         heap    portal    false    4            �            1259    167634    bookmakers_id_seq    SEQUENCE     �   CREATE SEQUENCE public.bookmakers_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 (   DROP SEQUENCE public.bookmakers_id_seq;
       public          portal    false    4    211            A           0    0    bookmakers_id_seq    SEQUENCE OWNED BY     G   ALTER SEQUENCE public.bookmakers_id_seq OWNED BY public.bookmakers.id;
          public          portal    false    210            �            1259    167673 	   referrals    TABLE     �   CREATE TABLE public.referrals (
    user_id integer,
    bookmaker_id integer NOT NULL,
    streamer_id integer NOT NULL,
    referral_key character varying NOT NULL,
    id integer NOT NULL
);
    DROP TABLE public.referrals;
       public         heap    portal    false    4            �            1259    167672    referrals_id_seq    SEQUENCE     �   CREATE SEQUENCE public.referrals_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 '   DROP SEQUENCE public.referrals_id_seq;
       public          portal    false    217    4            B           0    0    referrals_id_seq    SEQUENCE OWNED BY     E   ALTER SEQUENCE public.referrals_id_seq OWNED BY public.referrals.id;
          public          portal    false    216            �            1259    167701    streamer_bookmaker_membership    TABLE     �   CREATE TABLE public.streamer_bookmaker_membership (
    streamer_id integer NOT NULL,
    bookmaker_id integer NOT NULL,
    referral_link character varying NOT NULL,
    id integer NOT NULL
);
 1   DROP TABLE public.streamer_bookmaker_membership;
       public         heap    portal    false    4            �            1259    167700 $   streamer_bookmaker_membership_id_seq    SEQUENCE     �   CREATE SEQUENCE public.streamer_bookmaker_membership_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 ;   DROP SEQUENCE public.streamer_bookmaker_membership_id_seq;
       public          portal    false    219    4            C           0    0 $   streamer_bookmaker_membership_id_seq    SEQUENCE OWNED BY     m   ALTER SEQUENCE public.streamer_bookmaker_membership_id_seq OWNED BY public.streamer_bookmaker_membership.id;
          public          portal    false    218            �            1259    167646 	   streamers    TABLE     `   CREATE TABLE public.streamers (
    name character varying NOT NULL,
    id integer NOT NULL
);
    DROP TABLE public.streamers;
       public         heap    portal    false    4            �            1259    167645    streamers_id_seq    SEQUENCE     �   CREATE SEQUENCE public.streamers_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 '   DROP SEQUENCE public.streamers_id_seq;
       public          portal    false    213    4            D           0    0    streamers_id_seq    SEQUENCE OWNED BY     E   ALTER SEQUENCE public.streamers_id_seq OWNED BY public.streamers.id;
          public          portal    false    212            �            1259    167662    users    TABLE     �   CREATE TABLE public.users (
    telegram_id bigint NOT NULL,
    user_name text,
    first_name text,
    last_name text,
    language_code text,
    role public.role NOT NULL,
    id integer NOT NULL
);
    DROP TABLE public.users;
       public         heap    portal    false    841    4            �            1259    167661    users_id_seq    SEQUENCE     �   CREATE SEQUENCE public.users_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 #   DROP SEQUENCE public.users_id_seq;
       public          portal    false    4    215            E           0    0    users_id_seq    SEQUENCE OWNED BY     =   ALTER SEQUENCE public.users_id_seq OWNED BY public.users.id;
          public          portal    false    214            �           2604    167638    bookmakers id    DEFAULT     n   ALTER TABLE ONLY public.bookmakers ALTER COLUMN id SET DEFAULT nextval('public.bookmakers_id_seq'::regclass);
 <   ALTER TABLE public.bookmakers ALTER COLUMN id DROP DEFAULT;
       public          portal    false    210    211    211            �           2604    167676    referrals id    DEFAULT     l   ALTER TABLE ONLY public.referrals ALTER COLUMN id SET DEFAULT nextval('public.referrals_id_seq'::regclass);
 ;   ALTER TABLE public.referrals ALTER COLUMN id DROP DEFAULT;
       public          portal    false    216    217    217            �           2604    167704     streamer_bookmaker_membership id    DEFAULT     �   ALTER TABLE ONLY public.streamer_bookmaker_membership ALTER COLUMN id SET DEFAULT nextval('public.streamer_bookmaker_membership_id_seq'::regclass);
 O   ALTER TABLE public.streamer_bookmaker_membership ALTER COLUMN id DROP DEFAULT;
       public          portal    false    218    219    219            �           2604    167649    streamers id    DEFAULT     l   ALTER TABLE ONLY public.streamers ALTER COLUMN id SET DEFAULT nextval('public.streamers_id_seq'::regclass);
 ;   ALTER TABLE public.streamers ALTER COLUMN id DROP DEFAULT;
       public          portal    false    213    212    213            �           2604    167665    users id    DEFAULT     d   ALTER TABLE ONLY public.users ALTER COLUMN id SET DEFAULT nextval('public.users_id_seq'::regclass);
 7   ALTER TABLE public.users ALTER COLUMN id DROP DEFAULT;
       public          portal    false    215    214    215            -          0    167629    alembic_version 
   TABLE DATA           6   COPY public.alembic_version (version_num) FROM stdin;
    public          portal    false    209   �B       /          0    167635 
   bookmakers 
   TABLE DATA           .   COPY public.bookmakers (name, id) FROM stdin;
    public          portal    false    211   'C       5          0    167673 	   referrals 
   TABLE DATA           Y   COPY public.referrals (user_id, bookmaker_id, streamer_id, referral_key, id) FROM stdin;
    public          portal    false    217   SC       7          0    167701    streamer_bookmaker_membership 
   TABLE DATA           e   COPY public.streamer_bookmaker_membership (streamer_id, bookmaker_id, referral_link, id) FROM stdin;
    public          portal    false    219   pC       1          0    167646 	   streamers 
   TABLE DATA           -   COPY public.streamers (name, id) FROM stdin;
    public          portal    false    213   �C       3          0    167662    users 
   TABLE DATA           g   COPY public.users (telegram_id, user_name, first_name, last_name, language_code, role, id) FROM stdin;
    public          portal    false    215   �C       F           0    0    bookmakers_id_seq    SEQUENCE SET     ?   SELECT pg_catalog.setval('public.bookmakers_id_seq', 2, true);
          public          portal    false    210            G           0    0    referrals_id_seq    SEQUENCE SET     >   SELECT pg_catalog.setval('public.referrals_id_seq', 8, true);
          public          portal    false    216            H           0    0 $   streamer_bookmaker_membership_id_seq    SEQUENCE SET     R   SELECT pg_catalog.setval('public.streamer_bookmaker_membership_id_seq', 7, true);
          public          portal    false    218            I           0    0    streamers_id_seq    SEQUENCE SET     >   SELECT pg_catalog.setval('public.streamers_id_seq', 4, true);
          public          portal    false    212            J           0    0    users_id_seq    SEQUENCE SET     :   SELECT pg_catalog.setval('public.users_id_seq', 1, true);
          public          portal    false    214            �           2606    167633 #   alembic_version alembic_version_pkc 
   CONSTRAINT     j   ALTER TABLE ONLY public.alembic_version
    ADD CONSTRAINT alembic_version_pkc PRIMARY KEY (version_num);
 M   ALTER TABLE ONLY public.alembic_version DROP CONSTRAINT alembic_version_pkc;
       public            portal    false    209            �           2606    167642    bookmakers pk_bookmakers 
   CONSTRAINT     V   ALTER TABLE ONLY public.bookmakers
    ADD CONSTRAINT pk_bookmakers PRIMARY KEY (id);
 B   ALTER TABLE ONLY public.bookmakers DROP CONSTRAINT pk_bookmakers;
       public            portal    false    211            �           2606    167680    referrals pk_referrals 
   CONSTRAINT     T   ALTER TABLE ONLY public.referrals
    ADD CONSTRAINT pk_referrals PRIMARY KEY (id);
 @   ALTER TABLE ONLY public.referrals DROP CONSTRAINT pk_referrals;
       public            portal    false    217            �           2606    167708 >   streamer_bookmaker_membership pk_streamer_bookmaker_membership 
   CONSTRAINT     �   ALTER TABLE ONLY public.streamer_bookmaker_membership
    ADD CONSTRAINT pk_streamer_bookmaker_membership PRIMARY KEY (streamer_id, bookmaker_id, id);
 h   ALTER TABLE ONLY public.streamer_bookmaker_membership DROP CONSTRAINT pk_streamer_bookmaker_membership;
       public            portal    false    219    219    219            �           2606    167653    streamers pk_streamers 
   CONSTRAINT     T   ALTER TABLE ONLY public.streamers
    ADD CONSTRAINT pk_streamers PRIMARY KEY (id);
 @   ALTER TABLE ONLY public.streamers DROP CONSTRAINT pk_streamers;
       public            portal    false    213            �           2606    167669    users pk_users 
   CONSTRAINT     L   ALTER TABLE ONLY public.users
    ADD CONSTRAINT pk_users PRIMARY KEY (id);
 8   ALTER TABLE ONLY public.users DROP CONSTRAINT pk_users;
       public            portal    false    215            �           2606    167644    bookmakers uq_bookmakers_name 
   CONSTRAINT     X   ALTER TABLE ONLY public.bookmakers
    ADD CONSTRAINT uq_bookmakers_name UNIQUE (name);
 G   ALTER TABLE ONLY public.bookmakers DROP CONSTRAINT uq_bookmakers_name;
       public            portal    false    211            �           2606    167682 #   referrals uq_referrals_referral_key 
   CONSTRAINT     f   ALTER TABLE ONLY public.referrals
    ADD CONSTRAINT uq_referrals_referral_key UNIQUE (referral_key);
 M   ALTER TABLE ONLY public.referrals DROP CONSTRAINT uq_referrals_referral_key;
       public            portal    false    217            �           2606    167710 3   streamer_bookmaker_membership uq_streamer_bookmaker 
   CONSTRAINT     �   ALTER TABLE ONLY public.streamer_bookmaker_membership
    ADD CONSTRAINT uq_streamer_bookmaker UNIQUE (streamer_id, bookmaker_id);
 ]   ALTER TABLE ONLY public.streamer_bookmaker_membership DROP CONSTRAINT uq_streamer_bookmaker;
       public            portal    false    219    219            �           2606    167655    streamers uq_streamers_name 
   CONSTRAINT     V   ALTER TABLE ONLY public.streamers
    ADD CONSTRAINT uq_streamers_name UNIQUE (name);
 E   ALTER TABLE ONLY public.streamers DROP CONSTRAINT uq_streamers_name;
       public            portal    false    213            �           2606    167684    referrals uq_user_bookmaker 
   CONSTRAINT     g   ALTER TABLE ONLY public.referrals
    ADD CONSTRAINT uq_user_bookmaker UNIQUE (user_id, bookmaker_id);
 E   ALTER TABLE ONLY public.referrals DROP CONSTRAINT uq_user_bookmaker;
       public            portal    false    217    217            �           2606    167671    users uq_users_telegram_id 
   CONSTRAINT     \   ALTER TABLE ONLY public.users
    ADD CONSTRAINT uq_users_telegram_id UNIQUE (telegram_id);
 D   ALTER TABLE ONLY public.users DROP CONSTRAINT uq_users_telegram_id;
       public            portal    false    215            �           2606    167685 .   referrals fk_referrals_bookmaker_id_bookmakers    FK CONSTRAINT     �   ALTER TABLE ONLY public.referrals
    ADD CONSTRAINT fk_referrals_bookmaker_id_bookmakers FOREIGN KEY (bookmaker_id) REFERENCES public.bookmakers(id);
 X   ALTER TABLE ONLY public.referrals DROP CONSTRAINT fk_referrals_bookmaker_id_bookmakers;
       public          portal    false    211    217    3208            �           2606    167690 ,   referrals fk_referrals_streamer_id_streamers    FK CONSTRAINT     �   ALTER TABLE ONLY public.referrals
    ADD CONSTRAINT fk_referrals_streamer_id_streamers FOREIGN KEY (streamer_id) REFERENCES public.streamers(id);
 V   ALTER TABLE ONLY public.referrals DROP CONSTRAINT fk_referrals_streamer_id_streamers;
       public          portal    false    213    3212    217            �           2606    167695 $   referrals fk_referrals_user_id_users    FK CONSTRAINT     �   ALTER TABLE ONLY public.referrals
    ADD CONSTRAINT fk_referrals_user_id_users FOREIGN KEY (user_id) REFERENCES public.users(id);
 N   ALTER TABLE ONLY public.referrals DROP CONSTRAINT fk_referrals_user_id_users;
       public          portal    false    215    3216    217            �           2606    167711 V   streamer_bookmaker_membership fk_streamer_bookmaker_membership_bookmaker_id_bookmakers    FK CONSTRAINT     �   ALTER TABLE ONLY public.streamer_bookmaker_membership
    ADD CONSTRAINT fk_streamer_bookmaker_membership_bookmaker_id_bookmakers FOREIGN KEY (bookmaker_id) REFERENCES public.bookmakers(id);
 �   ALTER TABLE ONLY public.streamer_bookmaker_membership DROP CONSTRAINT fk_streamer_bookmaker_membership_bookmaker_id_bookmakers;
       public          portal    false    211    219    3208            �           2606    167716 T   streamer_bookmaker_membership fk_streamer_bookmaker_membership_streamer_id_streamers    FK CONSTRAINT     �   ALTER TABLE ONLY public.streamer_bookmaker_membership
    ADD CONSTRAINT fk_streamer_bookmaker_membership_streamer_id_streamers FOREIGN KEY (streamer_id) REFERENCES public.streamers(id);
 ~   ALTER TABLE ONLY public.streamer_bookmaker_membership DROP CONSTRAINT fk_streamer_bookmaker_membership_streamer_id_streamers;
       public          portal    false    3212    219    213            -      x�KI5M6N57OI36����� 18I      /      x�H,��4�����-�4����� :��      5      x������ � �      7   @   x�3�4��())(����HL*�K���4�2�&l�e�i�)l�e�M�ha3�!X�6����� x�(      1   %   x�+.)JM�M-�7�4�*�q�8�cNc�=... QnT      3      x������ � �     