--
-- PostgreSQL database dump
--

\restrict XAOo7CwTcvbrzB0upJSB9uslA1JIAtjBSqCRrLqWo4FNV2ctUwgiOpp2Z88gE5s

-- Dumped from database version 18.1 (Debian 18.1-1.pgdg13+2)
-- Dumped by pg_dump version 18.1 (Debian 18.1-1.pgdg13+2)

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET transaction_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: alembic_version; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE public.alembic_version (
    version_num character varying(32) NOT NULL
);


ALTER TABLE public.alembic_version OWNER TO admin;

--
-- Name: permissions; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE public.permissions (
    id integer NOT NULL,
    permission_name character varying NOT NULL
);


ALTER TABLE public.permissions OWNER TO admin;

--
-- Name: permissions_id_seq; Type: SEQUENCE; Schema: public; Owner: admin
--

CREATE SEQUENCE public.permissions_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.permissions_id_seq OWNER TO admin;

--
-- Name: permissions_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: admin
--

ALTER SEQUENCE public.permissions_id_seq OWNED BY public.permissions.id;


--
-- Name: profiles; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE public.profiles (
    user_id integer CONSTRAINT user_profiles_user_id_not_null NOT NULL,
    age character varying DEFAULT 'Не указано'::character varying CONSTRAINT user_profiles_age_not_null NOT NULL,
    date_of_birth character varying DEFAULT 'Не указано'::character varying CONSTRAINT user_profiles_date_of_birth_not_null NOT NULL,
    phone_number character varying DEFAULT 'Не указано'::character varying CONSTRAINT user_profiles_phone_number_not_null NOT NULL,
    bio text DEFAULT '...'::text CONSTRAINT user_profiles_bio_not_null NOT NULL
);


ALTER TABLE public.profiles OWNER TO admin;

--
-- Name: role_permissions; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE public.role_permissions (
    role_id integer NOT NULL,
    permission_id integer NOT NULL
);


ALTER TABLE public.role_permissions OWNER TO admin;

--
-- Name: roles; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE public.roles (
    id integer NOT NULL,
    role_name character varying NOT NULL
);


ALTER TABLE public.roles OWNER TO admin;

--
-- Name: roles_id_seq; Type: SEQUENCE; Schema: public; Owner: admin
--

CREATE SEQUENCE public.roles_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.roles_id_seq OWNER TO admin;

--
-- Name: roles_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: admin
--

ALTER SEQUENCE public.roles_id_seq OWNED BY public.roles.id;


--
-- Name: users; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE public.users (
    id integer NOT NULL,
    username character varying NOT NULL,
    first_name character varying NOT NULL,
    last_name character varying NOT NULL,
    middle_name character varying,
    email character varying NOT NULL,
    password character varying NOT NULL,
    is_active boolean DEFAULT true NOT NULL,
    role character varying DEFAULT USER NOT NULL
);


ALTER TABLE public.users OWNER TO admin;

--
-- Name: COLUMN users.middle_name; Type: COMMENT; Schema: public; Owner: admin
--

COMMENT ON COLUMN public.users.middle_name IS 'Отчество (при наличии)';


--
-- Name: COLUMN users.password; Type: COMMENT; Schema: public; Owner: admin
--

COMMENT ON COLUMN public.users.password IS 'Хеш пароля';


--
-- Name: users_id_seq; Type: SEQUENCE; Schema: public; Owner: admin
--

CREATE SEQUENCE public.users_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.users_id_seq OWNER TO admin;

--
-- Name: users_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: admin
--

ALTER SEQUENCE public.users_id_seq OWNED BY public.users.id;


--
-- Name: permissions id; Type: DEFAULT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.permissions ALTER COLUMN id SET DEFAULT nextval('public.permissions_id_seq'::regclass);


--
-- Name: roles id; Type: DEFAULT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.roles ALTER COLUMN id SET DEFAULT nextval('public.roles_id_seq'::regclass);


--
-- Name: users id; Type: DEFAULT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.users ALTER COLUMN id SET DEFAULT nextval('public.users_id_seq'::regclass);


--
-- Data for Name: alembic_version; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY public.alembic_version (version_num) FROM stdin;
d1e868c37b90
\.


--
-- Data for Name: permissions; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY public.permissions (id, permission_name) FROM stdin;
1	open_warehouse
2	root
3	string
5	testing.parseToken
6	testing.test
7	testing.update
\.


--
-- Data for Name: profiles; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY public.profiles (user_id, age, date_of_birth, phone_number, bio) FROM stdin;
6	25	09.09.2006	Не указано	...
7	22	Не указано	Не указано	Дата аналитик
8	Не указано	Не указано	Не указано	...
9	Не указано	Не указано	Не указано	...
10	44	Не указано	Не указано	...
\.


--
-- Data for Name: role_permissions; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY public.role_permissions (role_id, permission_id) FROM stdin;
3	2
6	1
11	5
11	6
11	7
\.


--
-- Data for Name: roles; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY public.roles (id, role_name) FROM stdin;
3	admin
6	test
9	user
11	tester
\.


--
-- Data for Name: users; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY public.users (id, username, first_name, last_name, middle_name, email, password, is_active, role) FROM stdin;
1	Jeson	Никита	Лаутеншлегер	Денисович	jeson.jesonov@gmail.com	$argon2id$v=19$m=65536,t=3,p=4$wOpkVaXTyO6fAi2xZrGchw$EEOfiqMdw9/6mbWXQHLrsssMyHscfAz20ccztzHzVAI	f	admin
6	sec	Albert	Popov	\N	user@example.com	$argon2id$v=19$m=65536,t=3,p=4$EnNdB2BAKlwApRsxxC6+eQ$9HIpv3cgc85jLLQlOByi0FDQusIZO+CH1r7zVEfNJrU	f	admin
7	jeks	Jason	Party	Eop	jey2210@mail.com	$argon2id$v=19$m=65536,t=3,p=4$JyUQg2ti0LGpOr27dXpEpA$fF4B2g9vYozZ7zQ+vGFD899omKjCMdsQyR3jX0knhUk	f	admin
8	kamila99	Kamila	Yongova	Olegovna	kkklll@gmail.com	$argon2id$v=19$m=65536,t=3,p=4$mom4WWWjK8JWcz96h1b37A$KGc5heSYJ/qU2IvXE2wasSM1m1DDJZ0kEV1IwTP0cmU	t	admin
9	jesk	jek	jekkk		user123@gmail.co	$argon2id$v=19$m=65536,t=3,p=4$En6XZ1a1Krxi159nKNF8OA$Z6Xpy1835mvWzvYrqA9P/q1l0ReJ6fO6mN0cGPhSD10	t	user
10	root	root	root	root	root@gmail.com	$argon2id$v=19$m=65536,t=3,p=4$cqj31Y1y2QM3BE/uOlgRFQ$v/xLZpxjlwLNNt7B/2OWYJyrwXdj288cLh40l0rL6T4	t	admin
\.


--
-- Name: permissions_id_seq; Type: SEQUENCE SET; Schema: public; Owner: admin
--

SELECT pg_catalog.setval('public.permissions_id_seq', 7, true);


--
-- Name: roles_id_seq; Type: SEQUENCE SET; Schema: public; Owner: admin
--

SELECT pg_catalog.setval('public.roles_id_seq', 11, true);


--
-- Name: users_id_seq; Type: SEQUENCE SET; Schema: public; Owner: admin
--

SELECT pg_catalog.setval('public.users_id_seq', 10, true);


--
-- Name: alembic_version alembic_version_pkc; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.alembic_version
    ADD CONSTRAINT alembic_version_pkc PRIMARY KEY (version_num);


--
-- Name: permissions permissions_permission_name_key; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.permissions
    ADD CONSTRAINT permissions_permission_name_key UNIQUE (permission_name);


--
-- Name: permissions permissions_pkey; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.permissions
    ADD CONSTRAINT permissions_pkey PRIMARY KEY (id);


--
-- Name: role_permissions role_permissions_pkey; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.role_permissions
    ADD CONSTRAINT role_permissions_pkey PRIMARY KEY (role_id, permission_id);


--
-- Name: roles roles_pkey; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.roles
    ADD CONSTRAINT roles_pkey PRIMARY KEY (id);


--
-- Name: roles roles_role_name_key; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.roles
    ADD CONSTRAINT roles_role_name_key UNIQUE (role_name);


--
-- Name: profiles user_profiles_pkey; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.profiles
    ADD CONSTRAINT user_profiles_pkey PRIMARY KEY (user_id);


--
-- Name: users users_email_key; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_email_key UNIQUE (email);


--
-- Name: users users_pkey; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_pkey PRIMARY KEY (id);


--
-- Name: users users_username_key; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_username_key UNIQUE (username);


--
-- Name: role_permissions role_permissions_permission_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.role_permissions
    ADD CONSTRAINT role_permissions_permission_id_fkey FOREIGN KEY (permission_id) REFERENCES public.permissions(id) ON DELETE CASCADE;


--
-- Name: role_permissions role_permissions_role_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.role_permissions
    ADD CONSTRAINT role_permissions_role_id_fkey FOREIGN KEY (role_id) REFERENCES public.roles(id) ON DELETE CASCADE;


--
-- Name: profiles user_profiles_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.profiles
    ADD CONSTRAINT user_profiles_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id) ON DELETE CASCADE;


--
-- PostgreSQL database dump complete
--

\unrestrict XAOo7CwTcvbrzB0upJSB9uslA1JIAtjBSqCRrLqWo4FNV2ctUwgiOpp2Z88gE5s

